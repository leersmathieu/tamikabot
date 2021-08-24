from discord.ext import commands
import sys
import math
import random
from art import *

list_type_ascii = ["block","","standard"]


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ascii', pass_context=True)
    async def ascii(self, ctx, *, entry):
        art_1 = text2art(str(entry),str(random.choice(list_type_ascii)))
        await ctx.send(f"```{art_1}```")




