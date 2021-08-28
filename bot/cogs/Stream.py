import discord
from discord import VoiceClient, ClientException, VoiceChannel
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.ext.commands.context import Context
import youtube_dl
import os


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', pass_context=True)
    async def play(self, ctx: Context, url: str, ):
        """
        Download one song from a given url and play it on your current discord channel
        """
        voiceChannel: VoiceChannel = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
        try:
            # Try to connect to a channel
            await voiceChannel.connect()
        except (PermissionError, ClientException) as error:
            print(f"Error: {error}")
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            # Stop the execution if one audio is already playing
            await ctx.send("Audio is already playing")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': 'True',

        }
        # Download, rename and play the song
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command(name='leave', pass_context=True)
    async def leave(self, ctx: Context):
        """
        Disconnect the bot from the current voice channel
        """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("Not connected")

    @commands.command(name='pause', pass_context=True)
    async def pause(self, ctx: Context):
        """
        Pause the audio
        """
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing")

    @commands.command(name='resume', pass_context=True)
    async def resume(self, ctx: Context):
        """
        Resume the audio
        """
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Audio not paused")

    @commands.command(name='stop', pass_context=True)
    async def stop(self, ctx: Context):
        """
        Stop the audio
        """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command(name='reset', pass_context=True)
    async def reset(self, ctx: Context):
        """
        Reset the bot by stopping and removing mp3 file and leaving the bot from this current channel
        """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await voice.disconnect()
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
