from discord.ext import commands
from commands.Del_messages import DeleteMessages
from commands.Google import Googlisation

from os import environ

# CONSTANTES
bot = commands.Bot(command_prefix="$")

bot.add_cog(DeleteMessages())
bot.add_cog(Googlisation())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 3)))


bot.run(environ.get('DISCORD_TOKEN'))
