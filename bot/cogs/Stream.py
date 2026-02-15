import asyncio
import shutil
import os
import discord
from discord import VoiceClient, ClientException
from discord.ext import commands
from discord.ext.commands.context import Context
import yt_dlp
import logging
from collections import deque
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Options yt-dlp : extraction d'URL uniquement, pas de téléchargement
YDL_OPTIONS = {
    'format': 'bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best',
    'noplaylist': True,
    'quiet': False,
    'no_warnings': False,
    'verbose': True,
    'default_search': 'ytsearch',
    'cookiefile': '/tmp/cookies.txt',
    'socket_timeout': 30,
    'retries': 3,
    'sleep_interval_requests': 1,  # 1s entre chaque requête HTTP vers YouTube
    'js_runtimes': {
        'node': {},
    },
    'remote_components': ['ejs:github'],
    'extractor_args': {
        'youtubepot-bgutilhttp': {
            'base_url': ['http://bgutil-provider:4416'],
        },
    },
}

# Options FFmpeg pour le streaming direct avec reconnexion limitée
FFMPEG_OPTIONS = {
    'before_options': (
        '-reconnect 1 -reconnect_streamed 1'
        ' -reconnect_delay_max 30'   # Attendre jusqu'à 30s entre les tentatives
        ' -reconnect_on_network_error 1'
        ' -reconnect_on_http_error 4xx,5xx'
    ),
    'options': '-vn',
}

# Délai entre les chansons pour éviter le spam YouTube (secondes)
QUEUE_DELAY = 2


class SongInfo:
    """Représente une chanson dans la queue."""

    def __init__(self, source_url: str, title: str, webpage_url: str):
        self.source_url = source_url
        self.title = title
        self.webpage_url = webpage_url

    @classmethod
    def from_ytdlp(cls, data: dict) -> 'SongInfo':
        """Crée un SongInfo à partir des données extraites par yt-dlp."""
        return cls(
            source_url=data.get('url', ''),
            title=data.get('title', 'Unknown'),
            webpage_url=data.get('webpage_url', ''),
        )


class Stream(commands.Cog):
    """Cog de lecture audio en streaming depuis YouTube (sans téléchargement de fichiers)."""

    COOKIES_SRC = '/opt/app/cookies.txt'
    COOKIES_DST = '/tmp/cookies.txt'

    def __init__(self, bot):
        self.bot = bot
        # Queue par guild (guild_id -> deque de SongInfo)
        self.queues: dict[int, deque[SongInfo]] = {}
        # Chanson en cours par guild
        self.current: dict[int, Optional[SongInfo]] = {}
        # Copier les cookies montés en read-only vers /tmp pour que yt-dlp puisse y écrire
        self._copy_cookies()
        logger.info("Stream Cog initialized")

    @staticmethod
    def _copy_cookies():
        """Copie le fichier cookies source (read-only) vers /tmp pour yt-dlp."""
        src = Stream.COOKIES_SRC
        dst = Stream.COOKIES_DST
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            logger.info(f"Cookies copied from {src} to {dst}")
        else:
            logger.warning(f"Cookies file not found at {src} — YouTube may block requests")

    # ── Helpers ──────────────────────────────────────────────────────

    def _get_queue(self, guild_id: int) -> deque[SongInfo]:
        """Retourne la queue d'une guild, la crée si nécessaire."""
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    @staticmethod
    def _extract_info(url: str) -> Optional[dict]:
        """Extrait les métadonnées audio d'une URL YouTube via yt-dlp (synchrone)."""
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            # Si c'est un résultat de recherche, prendre le premier résultat
            if 'entries' in info:
                info = info['entries'][0] if info['entries'] else None
            return info

    def _play_next(self, guild_id: int, voice: VoiceClient):
        """Callback appelé quand une chanson se termine — joue la suivante dans la queue."""
        queue = self._get_queue(guild_id)
        if queue:
            next_song = queue.popleft()
            self.current[guild_id] = next_song

            async def _delayed_play():
                await asyncio.sleep(QUEUE_DELAY)  # Délai anti-spam YouTube
                if voice.is_connected():
                    source = discord.FFmpegPCMAudio(next_song.source_url, **FFMPEG_OPTIONS)
                    voice.play(source, after=lambda e: self._play_next(guild_id, voice))
                    logger.info(f"Playing next in queue: {next_song.title}")

            asyncio.run_coroutine_threadsafe(_delayed_play(), self.bot.loop)
        else:
            self.current.pop(guild_id, None)
            self.queues.pop(guild_id, None)
            logger.info("Queue empty, disconnecting from voice channel")
            asyncio.run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)

    # ── Commandes ────────────────────────────────────────────────────

    @commands.command(name='play')
    @commands.cooldown(1, 5, commands.BucketType.guild)  # 1 commande par 5 secondes par serveur
    async def play(self, ctx: Context, *, query: str):
        """
        Joue un audio YouTube en streaming. Accepte une URL ou des mots-clés de recherche.
        Si un audio est déjà en cours, ajoute à la queue.
        """
        logger.info(f"Received play command with query: {query}")

        if not ctx.author.voice:
            await ctx.send("Tu n'es pas connecté à un salon vocal.")
            return

        voice_channel = ctx.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        # Nettoyage d'une connexion vocale périmée avant de reconnecter
        if voice is not None and not voice.is_connected():
            try:
                voice.cleanup()
                await voice.disconnect(force=True)
            except Exception:
                pass
            voice = None

        # Connexion au salon vocal si nécessaire
        if voice is None:
            try:
                voice = await voice_channel.connect(self_deaf=True)
                logger.info(f"Connected to voice channel: {voice_channel.name}")
            except Exception as error:
                logger.error(f"Error connecting to voice channel: {error}")
                await ctx.send(f"Error connecting to voice channel: {error}")
                return
        elif voice.channel != voice_channel:
            await voice.move_to(voice_channel)

        # Extraction des infos audio dans un thread séparé (bloquant → run_in_executor)
        # await ctx.send(f"🔎 Searching: **{query}**...")
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, self._extract_info, query)
        except Exception as e:
            logger.error(f"Error extracting audio info: {e}")
            await ctx.send(f"Error extracting audio: {e}")
            return

        if info is None:
            await ctx.send("Aucun résultat trouvé.")
            return

        song = SongInfo.from_ytdlp(info)
        guild_id = ctx.guild.id

        # Si déjà en lecture, ajouter à la queue
        if voice.is_playing() or voice.is_paused():
            queue = self._get_queue(guild_id)
            queue.append(song)
            position = len(queue)
            await ctx.send(f"📋 Added to queue (#{position}): **{song.title}**")
            logger.info(f"Queued: {song.title} (position {position})")
            return

        # Lecture directe
        self.current[guild_id] = song
        source = discord.FFmpegPCMAudio(song.source_url, **FFMPEG_OPTIONS)
        voice.play(source, after=lambda e: self._play_next(guild_id, voice))
        await ctx.send(f"🎵 Now playing: **{song.title}**")
        logger.info(f"Now playing: {song.title}")

    @commands.command(name='skip')
    async def skip(self, ctx: Context):
        """Passe à la chanson suivante dans la queue."""
        logger.info("Received skip command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()  # Déclenche le callback _play_next
            await ctx.send("⏭ Chanson passée.")
        else:
            await ctx.send("Rien n'est en cours de lecture.")

    @commands.command(name='queue')
    async def queue(self, ctx: Context):
        """Affiche la queue de lecture."""
        guild_id = ctx.guild.id
        current = self.current.get(guild_id)
        queue = self._get_queue(guild_id)

        if not current and not queue:
            await ctx.send("La queue est vide.")
            return

        lines = []
        if current:
            lines.append(f"🎵 **En cours:** {current.title}")
        for i, song in enumerate(queue, start=1):
            lines.append(f"`{i}.` {song.title}")

        await ctx.send("\n".join(lines))

    @commands.command(name='leave')
    async def leave(self, ctx: Context):
        """Déconnecte le bot du salon vocal et vide la queue."""
        logger.info("Received leave command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            guild_id = ctx.guild.id
            self.queues.pop(guild_id, None)
            self.current.pop(guild_id, None)
            voice.stop()
            voice.cleanup()
            await voice.disconnect()
            logger.info("Disconnected from voice channel")
        else:
            await ctx.send("Non connecté")

    @commands.command(name='pause')
    async def pause(self, ctx: Context):
        """Met l'audio en pause."""
        logger.info("Received pause command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("⏸ En pause.")
        else:
            await ctx.send("Aucun audio en cours de lecture")

    @commands.command(name='resume')
    async def resume(self, ctx: Context):
        """Reprend l'audio en pause."""
        logger.info("Received resume command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("▶ Repris.")
        else:
            await ctx.send("L'audio n'est pas en pause")

    @commands.command(name='stop')
    async def stop(self, ctx: Context):
        """Arrête l'audio et vide la queue."""
        logger.info("Received stop command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            guild_id = ctx.guild.id
            self.queues.pop(guild_id, None)
            self.current.pop(guild_id, None)
            voice.stop()
            await ctx.send("⏹ Arrêté.")
        else:
            await ctx.send("Non connecté")

    @commands.command(name='reset')
    async def reset(self, ctx: Context):
        """Arrête l'audio, vide la queue et déconnecte le bot du salon vocal."""
        logger.info("Received reset command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            guild_id = ctx.guild.id
            self.queues.pop(guild_id, None)
            self.current.pop(guild_id, None)
            voice.stop()
            voice.cleanup()
            await voice.disconnect()
            logger.info("Reset complete")
            await ctx.send("🔄 Réinitialisation terminée.")
        else:
            await ctx.send("Non connecté")

    # ── Gestionnaire d'erreurs ─────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        """Gère les erreurs de cooldown."""
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ Attends {error.retry_after:.1f}s avant de réutiliser cette commande.")
        else:
            # Laisser les autres erreurs se propager
            raise error
