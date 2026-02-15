import asyncio
from discord.ext import commands
from discord.ext.commands.context import Context

from ..config import Config


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config = Config()
        self.admin_id = int(config.ADMIN_ID) if config.ADMIN_ID else None

    @commands.command(name='del_messages')
    async def delete_messages(self, ctx: Context, number_of_messages: int):
        """
        Supprime X messages du salon actuel
        """
        if ctx.message.author.guild_permissions.manage_messages:
            messages = [m async for m in ctx.channel.history(limit=number_of_messages + 1)]
            for message in messages:
                print(f'deleted messages :{message.content}')
                await message.delete()
                await asyncio.sleep(0.5)  # Delay to avoid Discord rate limiting
        else:
            await ctx.send('Permission denied!')

    @commands.command(name='say')
    async def say(self, ctx: Context, chan_id: int, *, text: str):
        """
        Le bot envoie un message dans un salon donné
        """
        # Don't respond to ourselves
        if ctx.message.author == self.bot.user:
            return

        # Don't respond to any bot
        if ctx.message.author.bot:
            return

        if self.admin_id and ctx.message.author.id == self.admin_id:

            try:
                channel = self.bot.get_channel(chan_id)
                await channel.send(text)

            except Exception as error:
                print(error)
                await ctx.send('Invalid Way')

