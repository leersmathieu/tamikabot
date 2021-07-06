from discord.ext import commands

from bot.cogs.Messages import Messages
from bot.cogs.Google import Google
from bot.cogs.Joke import Joke

# CONSTANTES
bot = commands.Bot(command_prefix="/")

bot.add_cog(Messages(bot))
bot.add_cog(Google())
bot.add_cog(Joke())



@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 3)))


bot.run("NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI")
