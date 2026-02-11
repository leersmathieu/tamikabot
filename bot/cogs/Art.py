from discord.ext import commands
from discord.ext.commands.context import Context

import sys
import math
import random
from art import *

list_type_ascii = ["","standard"]


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ascii')
    async def ascii(self, ctx: Context, *, sentences: str):
        """
        Transform a given sentence by ascii art
        """
        art_1 = text2art(str(sentences),str(random.choice(list_type_ascii)))
        await ctx.send(f"```{art_1}```")




