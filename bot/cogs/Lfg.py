from discord.ext import commands
from discord.ext.commands.context import Context

from discord import utils

import random

class Lfg(commands.Cog):
    def __init__(self, bot, sentences: list):
        self.bot = bot
        self.sentences = sentences

    @commands.cooldown(1, 2700, commands.BucketType.default)
    @commands.command(name="recherche", pass_context=True)
    async def looking_for_group(self, ctx: Context):
        """
        Looking for group systeme for Payday2france Discord
        """

        mesage_author = ctx.author.id
        role = utils.get(ctx.guild.roles, name="Recherche joueurs")

        rand_int = int(random.randrange(0, len(self.sentences)))
        random_sentences = self.sentences[rand_int]
        sentences_with_mention = random_sentences.replace("{}", f"<@{mesage_author}>" )

        try:
            if role in ctx.message.author.roles:
                await ctx.send(sentences_with_mention)
            else:
                await ctx.send("Tu ne possèdes pas le rôle 'Recherche joueurs' (tu peux le récupérer dans <#636998523694350336>)")
                
        except Exception as error:
            print(error)
            await ctx.send("Il y a un bug dans votre simulation qui ne me permet pas d'exécuter correctement ce que vous me demandez.")



