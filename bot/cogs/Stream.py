import discord
from discord import VoiceClient, ClientException, VoiceChannel
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ext.commands.context import Context
import yt_dlp
import os
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# discord_logger = logging.getLogger('discord')
# discord_logger.setLevel(logging.DEBUG)

class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Stream Cog initialized")

    @commands.command(name='play')
    async def play(self, ctx: Context, url: str):
        """
        Download one song from a given url and play it on your current discord channel
        """
        logger.info(f"Received play command with URL: {url}")

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            logger.info("Author not connected to a voice channel.")
            return

        voice_channel = ctx.author.voice.channel
        try:
            logger.info(f"Attempting to connect to voice channel: {voice_channel.name}")
            await voice_channel.connect()
        except (PermissionError, ClientException) as error:
            logger.error(f"Error connecting to voice channel: {error}")
            await ctx.send(f"Error connecting to voice channel: {error}")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            logger.info("Audio is already playing")
            await ctx.send("Audio is already playing")
            return

        # Assurez-vous qu'aucun fichier précédent n'interfère
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                logger.info(f"Removing previous file: {file}")
                os.remove(file)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': 'True',
            'concurrent-fragments': 5,
            'throttled-rate': '1M',
        }

        logger.info(f"Downloading audio from URL: {url}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            await ctx.send(f"Error downloading audio: {e}")
            return

        # Vérifier que le fichier a été téléchargé
        downloaded_file = None
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                downloaded_file = file
                break

        if not downloaded_file:
            logger.error("No mp3 file found after download")
            await ctx.send("Failed to download audio.")
            return

        logger.info(f"Renaming downloaded file to song.mp3: {downloaded_file}")
        os.rename(downloaded_file, "song.mp3")

        logger.info("Playing audio: song.mp3")
        try:
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send("Playing your song.")
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            await ctx.send(f"Error playing audio: {e}")

    @commands.command(name='leave')
    async def leave(self, ctx: Context):
        """
        Disconnect the bot from the current voice channel
        """
        logger.info("Received leave command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            logger.info("Disconnecting from voice channel")
            voice.cleanup()
            await voice.disconnect()
        else:
            logger.info("Bot not connected to any voice channel")
            await ctx.send("Not connected")

    @commands.command(name='pause')
    async def pause(self, ctx: Context):
        """
        Pause the audio
        """
        logger.info("Received pause command")
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            logger.info("Pausing audio")
            voice.pause()
        else:
            logger.info("No audio is playing")
            await ctx.send("No audio is playing")

    @commands.command(name='resume')
    async def resume(self, ctx: Context):
        """
        Resume the audio
        """
        logger.info("Received resume command")
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            logger.info("Resuming audio")
            voice.resume()
        else:
            logger.info("Audio not paused")
            await ctx.send("Audio not paused")

    @commands.command(name='stop')
    async def stop(self, ctx: Context):
        """
        Stop the audio
        """
        logger.info("Received stop command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            logger.info("Stopping audio")
            voice.stop()
        else:
            logger.info("No audio to stop")

    @commands.command(name='reset')
    async def reset(self, ctx: Context):
        """
        Reset the bot by stopping and removing mp3 file and leaving the bot from this current channel
        """
        logger.info("Received reset command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice:
            logger.info("Stopping audio and disconnecting")
            voice.stop()
            voice.cleanup()
            await voice.disconnect()
            
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                logger.info(f"Removing file: {file}")
                os.remove(file)
