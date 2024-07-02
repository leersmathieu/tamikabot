import discord
from discord import VoiceClient, ClientException, VoiceChannel
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ext.commands.context import Context
import youtube_dl
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

    @commands.command(name='play', pass_context=True)
    async def play(self, ctx: Context, url: str):
        """
        Download one song from a given url and play it on your current discord channel
        """
        logger.info("Received play command with URL: %s", url)

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            logger.info("Author not connected to a voice channel.")
            return

        voice_channel = ctx.author.voice.channel
        try:
            logger.info("Attempting to connect to voice channel: %s", voice_channel.name)
            await voice_channel.connect()
        except (PermissionError, ClientException) as error:
            logger.error("Error connecting to voice channel: %s", error)
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
                logger.info("Removing previous file: %s", file)
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

        logger.info("Downloading audio from URL: %s", url)
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.error("Error downloading audio: %s", e)
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

        logger.info("Renaming downloaded file to song.mp3: %s", downloaded_file)
        os.rename(downloaded_file, "song.mp3")

        logger.info("Playing audio: song.mp3")
        try:
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send("Playing your song.")
        except Exception as e:
            logger.error("Error playing audio: %s", e)
            await ctx.send(f"Error playing audio: {e}")

    @commands.command(name='leave', pass_context=True)
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
            voice.cleanup()
            logger.info("Bot not connected to any voice channel")
            await ctx.send("Not connected")

    @commands.command(name='pause', pass_context=True)
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

    @commands.command(name='resume', pass_context=True)
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

    @commands.command(name='stop', pass_context=True)
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

    @commands.command(name='reset', pass_context=True)
    async def reset(self, ctx: Context):
        """
        Reset the bot by stopping and removing mp3 file and leaving the bot from this current channel
        """
        logger.info("Received reset command")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice:
            logger.info("Stopping audio and disconnecting")
            voice.cleanup()
            await voice.stop()
            await voice.disconnect()
            
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                logger.info("Removing file: %s", file)
                os.remove(file)
