from discord.ext import commands
from discord.ext.commands.context import Context

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg=f"Rechargement de mes ressources, veuillez patienter encore {round(error.retry_after)}s avant de retenter cette action"
            await ctx.send(msg)

    @commands.Cog.listener()
    async def on_ready(self):
        """Triggered when the bot connects to Discord."""

        print('Ready!')

