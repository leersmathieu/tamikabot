from collections import defaultdict

from discord.ext import commands
from discord.message import Message

from .cogs import Google
from .cogs import Art
from .cogs import Joke
from .cogs import Bank
from .cogs import Stream
from .cogs import Messages
from .cogs import Lfg
from .config import Config
from .events import Events
from .lfg_sentences import lfg_sentences  # Importation des phrases

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config()

# database = Database(config.DB_HOST, config.DB_PASSWORD)

# Doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
class Bot(commands.Bot):

    def __init__(self):
        commands_prefixes = ['$']
    
        super().__init__(commands_prefixes)

        self.token = config.TOKEN
        self.history = defaultdict(lambda: False)

        # Register all Cogs
        self.add_cog(Messages(self))
        self.add_cog(Google(self))
        self.add_cog(Joke(self))
        self.add_cog(Art(self))
        self.add_cog(Bank(self))
        self.add_cog(Lfg(self, lfg_sentences))
        self.add_cog(Stream(self))
        logger.info("Stream Cog added")

        # Register personal events
        self.add_cog(Events(self))

    def run(self):
        """
        Override the run method to pass the token directly from self.token.
        """
        logger.info("Running bot with token")
        # Connect the bot to Discord servers
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
