from discord.ext import commands


class DeleteMessages(commands.Cog):

    @commands.command(name='del_messages')
    async def delete_messages(self, ctx, number_of_messages: int):
        if ctx.message.author.guild_permissions.manage_messages:
            messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
            for message in messages:
                print(message.content)
                await message.delete()
        else:
            await ctx.send('Permission denied!')
