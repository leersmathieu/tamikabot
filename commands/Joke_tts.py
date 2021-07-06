from discord.ext import commands
import pandas
import random
import base64


class JokeTts(commands.Cog):

    @commands.command(name='joke_tts')
    async def say_joke(self, ctx):
        df = pandas.read_csv("./db/joke.csv", sep=" ")
        rnumber = random.randint(1, len(df))
        decoding = base64.b64decode(df.iloc[rnumber, 0])
        await ctx.send(decoding.decode("utf-8"), tts=True)

