from discord.ext import commands
from discord.ext.commands.context import Context
import pandas
import random
import base64


class Joke(commands.Cog):

    @commands.command(name='joke')
    async def say_joke(self, ctx: Context):
        """
        The bot say a random joke
        """
        df = pandas.read_csv("./bot/db/joke.csv", sep=" ")
        rnumber = random.randint(1, len(df))
        decoding = base64.b64decode(df.iloc[rnumber, 0])
        await ctx.send(decoding.decode("utf-8"))

    @commands.command(name='joke_tts')
    async def say_joke_tts(self, ctx: Context):
        """
        The bot say a random joke with text to speech active
        """
        df = pandas.read_csv("./bot/db/joke.csv", sep=" ")
        rnumber = random.randint(1, len(df))
        decoding = base64.b64decode(df.iloc[rnumber, 0])
        await ctx.send(decoding.decode("utf-8"), tts=True)
