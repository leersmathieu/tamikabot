from discord.ext import commands
import pandas
import random
import base64
import requests


class Joke(commands.Cog):

    @commands.command(name='joke')
    async def say_joke(self, ctx):
        df = pandas.read_csv("./bot/db/joke.csv", sep=" ")
        rnumber = random.randint(1, len(df))
        decoding = base64.b64decode(df.iloc[rnumber, 0])
        await ctx.send(decoding.decode("utf-8"))


    # @commands.command(name='joke_tts')
    # async def say_joke_tts(self, ctx):
    #     df = pandas.read_csv("./bot/db/joke.csv", sep=" ")
    #     rnumber = random.randint(1, len(df))
    #     decoding = base64.b64decode(df.iloc[rnumber, 0])
    #     await ctx.send(decoding.decode("utf-8"), tts=True)

# class SetupJoke:
#     def say_joke(self):
#
#         url = "https://discord.com/api/v8/applications/469072242865602561/guilds/430139146028187658/commands"  # guild specified
#         json = {
#             "name": "joke",
#             "description": "Send a random funny joke",
#         }
#
#         # For authorization
#         headers = {
#             "Authorization": "Bot NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI"
#         }
#
#         r = requests.post(url, headers=headers, json=json)
#         print(r)
#
#     def setup(self):
#         self.say_joke()