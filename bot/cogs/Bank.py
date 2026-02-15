from discord.ext import commands
from discord.ext.commands.context import Context
import re
import logging

from ..config import Config
from ..db.database import BankDatabase

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config = Config()
        self.admin_id = int(config.ADMIN_ID) if config.ADMIN_ID else None
        self.db = BankDatabase()
        logger.info("Bank database initialized successfully.")

    @commands.command(name='add_coins')
    async def add_coins(self, ctx: Context, user: str, amount: int):
        """
        Ajoute (ou retire si nombre négatif) un montant de coins à un utilisateur
        """
        user_id = str(re.findall(r'\b\d+\b', user)[0])
        user_mention = await self.bot.fetch_user(int(user_id))

        if self.admin_id and ctx.message.author.id == self.admin_id:
            try:
                new_balance = self.db.add_coins(user_id, amount)
                await ctx.send(f"{user_mention.mention} gagne {amount} coins !")
                logger.info(f"Added {amount} coins to user {user_id}. New balance: {new_balance}")
            except Exception as error:
                logger.error(f"Error adding coins: {error}")
                await ctx.send("Une erreur est survenue lors de l'ajout de coins.")
        else:
            await ctx.send(f"{user_mention.mention} dont try to break the rules!")

    @commands.command(name='bank')
    async def bank(self, ctx: Context):
        """
        Consulte ton compte en banque
        """
        user_id = str(ctx.author.id)
        balance = self.db.get_balance(user_id)
        
        if balance is not None:
            await ctx.send(f"Tu as {balance} coins")
        else:
            await ctx.send("Tu n'as pas de compte en banque !")