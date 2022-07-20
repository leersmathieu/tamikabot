from discord.ext import commands
from discord.ext.commands.context import Context

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg="Rechargement de mes ressources, veuillez patienter encore {:.2f}s avant de retenter cette action".format(error.retry_after)
            await ctx.send(msg)



