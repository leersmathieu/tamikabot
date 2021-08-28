from collections import defaultdict

from discord.ext import commands
from discord.message import Message

from .cogs import Google
from .cogs import Art
from .cogs import Joke
from .cogs import Bank
from .cogs import Stream
from .cogs import Messages
from .config import Config

# from discord_slash import SlashCommand
# from .cogs import SetupJoke

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
        self.add_cog(Stream(self))



        # self.setup_commands()

    # def setup_commands(self):
    #     SetupJoke().setup()

    def run(self):
        """
        Override the run method to pass the token directly from self.token.
        """

        # Connect the bot to Discord servers
        super(Bot, self).run(self.token)

    async def on_ready(self):
        """Triggered when the bot connects to Discord."""

        # Print a confirmation message to the console
        print(f'Bot connected to Discord with id: "{self.user}".')

    async def on_message(self, message: Message):
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

        # Trigger the Cogs
        await super(Bot, self).on_message(message)
