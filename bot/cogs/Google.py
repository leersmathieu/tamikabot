from discord.ext import commands

import urllib.parse


class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='google', pass_context=True)
    async def google_search(self, ctx, *, entry):
        # Note for *, it tells the library to put everything
        # the user types after it into message as a string.

        try:
            url = urllib.parse.quote(entry)
            await ctx.send('https://www.google.com/search?q=' + url)

        except Exception as error:
            print(error)
            ctx.send('Invalid URL')
