import discord
from discord import VoiceClient, ClientException
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

        # song_there = os.path.isfile("song.mp3")
        # try:
        #     if song_there:
        #         os.remove("song.mp3")
        # except (PermissionError, CommandInvokeError, ClientException):
        #     await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        #     return

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Général')
        try:
            # Try to connect to a channel
            await voiceChannel.connect()
        except (PermissionError, ClientException) as error:
            print(f"Error: {error}")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
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
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command(name='leave', pass_context=True)
    async def leave(self, ctx: Context):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("Not connected")

    @commands.command(name='pause', pass_context=True)
    async def pause(self, ctx: Context):
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing")

    @commands.command(name='resume', pass_context=True)
    async def resume(self, ctx: Context):
        voice: VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Audio not paused")

    @commands.command(name='stop', pass_context=True)
    async def stop(self, ctx: Context):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command(name='reset', pass_context=True)
    async def reset(self, ctx: Context):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await voice.disconnect()
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
