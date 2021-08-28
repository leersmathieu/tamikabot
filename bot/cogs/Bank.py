from discord.ext import commands
from discord.ext.commands.context import Context
import pickle
import pandas as pd
import re


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tamikara_id = 183999045168005120
        with open('./bot/db/filename.pickle', 'rb') as handle:
            self.db: pd.DataFrame = pickle.load(handle)

    @commands.command(name='add_coins', pass_context=True)
    async def add_coins(self, ctx: Context, user: str, amount: int):
        """
        Add ( or remove if negative number ) a given amount of coins for the given user
        """
        user = str(re.findall(r'\b\d+\b', user)[0])
        user_mention = await self.bot.fetch_user(int(user))

        if ctx.message.author.id == self.tamikara_id:
            try:
                if user in self.db.index.tolist():
                    self.db.at[user, 'bank'] += int(amount)

                else:
                    self.db = self.db.append(pd.Series({'bank': int(amount)}, name=user))

                # print(self.db)
                with open('./bot/db/filename.pickle', 'wb') as handle:
                    pickle.dump(self.db, handle)

                await ctx.send(f"{user_mention.mention} gagne {amount} coins !")

            except Exception as error:
                print(error)
        else:
            await ctx.send(f"{user_mention.mention} dont try to break the rules!")

    @commands.command(name='bank', pass_context=True)
    async def bank(self, ctx: Context):
        """
        See your bank account
        """
        try:
            await ctx.send(f"Tu as {self.db.loc[str(ctx.author.id), 'bank']} coins")

        except Exception as error:
            print(f"error: {error}")
            await ctx.send("Tu n'as pas de compte en banque !")