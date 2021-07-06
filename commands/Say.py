from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tamikara_id = 183999045168005120

    @commands.command(name='say', pass_context=True)
    async def say(self, ctx, chan_id: int, *, text):

        # Don't respond to ourselves
        if ctx.message.author == self.bot.user:
            return

        # Don't respond to any bot
        if ctx.message.author.bot:
            return

        if ctx.message.author.id == self.tamikara_id:

            try:
                channel = self.bot.get_channel(chan_id)
                await channel.send(text)

            except Exception as error:
                print(error)
                await ctx.send('Invalid Way')
