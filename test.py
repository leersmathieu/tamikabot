# bot.py
import discord

from discord_slash import SlashCommand
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

bot = commands.Bot(command_prefix="prefix")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

# bot.load_extension("cog")


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])

print("start")
bot.add_cog(Slash(bot))
bot.run("NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI")
print("ok")
