from discord.ext import commands
from discord.ext.commands.context import Context


class Lfg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lfg', pass_context=True)
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def looking_for_group(self, ctx: Context):
        """
        Looking for group systeme for Payday2france Discord
        """

        mesage_author = ctx.author.id
        await ctx.send(f'Avis à la <@&973556338275799120>, <@{mesage_author}> a besoin de vous, là, maintenant !')
