from discord.ext import commands
from os import environ

from commands.DeleteMessages import DeleteMessages
from commands.Google import Googlisation
from commands.Say import Say
from commands.Joke import Joke
from commands.Joke_tts import JokeTts

# CONSTANTES
bot = commands.Bot(command_prefix="$")

bot.add_cog(DeleteMessages())
bot.add_cog(Googlisation())
bot.add_cog(Say(bot))
bot.add_cog(Joke())
bot.add_cog(JokeTts())



@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 3)))


bot.run("NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI")
