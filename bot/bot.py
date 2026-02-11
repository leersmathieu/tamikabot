from collections import defaultdict

import discord
from discord.ext import commands

from .cogs import Google
from .cogs import Art
from .cogs import Joke
from .cogs import Bank
from .cogs import Stream
from .cogs import Messages
from .config import Config
from .events import Events

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config()

# Doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix='$', intents=intents)

        self.token = config.TOKEN
        self.history = defaultdict(lambda: False)

    async def setup_hook(self):
        """
        Called once the bot is logged in but before connecting to the gateway.
        Used to register all Cogs asynchronously (required in discord.py 2.x).
        """
        await self.add_cog(Messages(self))
        await self.add_cog(Google(self))
        await self.add_cog(Joke(self))
        await self.add_cog(Art(self))
        await self.add_cog(Bank(self))
        await self.add_cog(Stream(self))
        await self.add_cog(Events(self))
        logger.info("All Cogs loaded")

    def run(self):
        """
        Override the run method to pass the token directly from self.token.
        """
        logger.info("Running bot with token")
        super(Bot, self).run(self.token)

    async def on_message(self, message):
        """
        Triggered when a message is send on any channel/server that the
        bot have access.
        """

        # Don't respond to ourselves
        if message.author == self.user:
            return

        # Don't respond to any bot
        if message.author.bot:
            return

        channel_name = getattr(message.channel, 'name', 'DM')
        logger.info(f"Message from {message.author.name} in {channel_name}: {message.content}")

        # Process commands
        await self.process_commands(message)
