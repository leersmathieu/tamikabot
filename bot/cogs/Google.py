from discord.ext import commands
from discord.ext.commands.context import Context

import urllib.parse

from googletrans import Translator, constants


class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # init the Google API translator
        self.translator = Translator()

    @commands.command(name='google')
    async def google_search(self, ctx: Context, *, entry: str):
        """
        Effectue une recherche Google à partir d'une requête
        """
        # Note for *, it tells the library to put everything
        # the user types after it into message as a string.
        try:
            url = urllib.parse.quote(entry)
            await ctx.send('https://www.google.com/search?q=' + url)

        except Exception as error:
            print(error)
            ctx.send('Invalid URL')

    @commands.command(name='translate')
    async def translate(self, ctx: Context, language: str, *, sentences: str):
        """
        Traduit un texte vers une langue donnée
        """
        translator = self.translator
        translation = translator.translate(sentences, dest=language)
        await ctx.send(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")