from discord.ext import commands
from googletrans import Translator, constants

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tamikara_id = 183999045168005120

        # init the Google API translator
        self.translator = Translator()

    @commands.command(name='del_messages')
    async def delete_messages(self, ctx, number_of_messages: int):
        if ctx.message.author.guild_permissions.manage_messages:
            messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
            for message in messages:
                print(f'deleted messages :{message.content}')
                await message.delete()
        else:
            await ctx.send('Permission denied!')

    @commands.command(name='translate')
    async def translate(self, ctx, language: str, *, sentences: str):
        translator = self.translator
        translation = translator.translate(sentences, dest=language)
        await ctx.send(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

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

