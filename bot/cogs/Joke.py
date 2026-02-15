from discord.ext import commands
from discord.ext.commands.context import Context
import random
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Joke(commands.Cog):

    def _load_jokes(self):
        """Load jokes from CSV file."""
        with open("./bot/db/joke.csv", "r", encoding="utf-8") as f:
            jokes = [line.strip() for line in f if line.strip()]
        return jokes

    @commands.command(name='joke')
    async def say_joke(self, ctx: Context):
        """
        Le bot raconte une blague aléatoire
        """
        logger.info("requesting joke")
        jokes = self._load_jokes()
        joke_encoded = random.choice(jokes)
        decoding = base64.b64decode(joke_encoded)
        await ctx.send(decoding.decode("utf-8"))

    @commands.command(name='joke_tts')
    async def say_joke_tts(self, ctx: Context):
        """
        Le bot raconte une blague aléatoire avec synthèse vocale
        """
        jokes = self._load_jokes()
        joke_encoded = random.choice(jokes)
        decoding = base64.b64decode(joke_encoded)
        await ctx.send(decoding.decode("utf-8"), tts=True)
