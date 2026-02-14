import random
import logging

from discord import utils
from discord.ext import commands
from discord.ext.commands import Context

from bot.lfg_sentences import lfg_sentences

logger = logging.getLogger(__name__)

LFG_ROLE_NAME = "Recherche joueurs"
LFG_COOLDOWN_SECONDS = 2700  # 45 minutes


class Lfg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sentences = lfg_sentences

    @commands.cooldown(1, LFG_COOLDOWN_SECONDS, commands.BucketType.default)
    @commands.command(name="recherche")
    async def looking_for_group(self, ctx: Context):
        """Envoie un message LFG aléatoire mentionnant l'auteur (nécessite le rôle 'Recherche joueurs').
        
        *Conçu spécifiquement pour le serveur Payday2France Discord.*"""
        role = utils.get(ctx.guild.roles, name=LFG_ROLE_NAME)

        if role is None:
            await ctx.send(f"Le rôle '{LFG_ROLE_NAME}' n'existe pas sur ce serveur.")
            return

        if role not in ctx.author.roles:
            await ctx.send(f"Tu ne possèdes pas le rôle '{LFG_ROLE_NAME}'.")
            return

        sentence = random.choice(self.sentences)
        message = sentence.replace("{}", f"<@{ctx.author.id}>")
        await ctx.send(message)

