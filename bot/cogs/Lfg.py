from discord.ext import commands
from discord.ext.commands.context import Context


class Lfg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lfg', pass_context=True)
    async def google_search(self, ctx: Context):
        """
        Looking for group systeme for Payday2france Discord
        """
        try:
            await ctx.send('recherche de groupe')

        except Exception as error:
            print(error)
            ctx.send('Not avalaible')
