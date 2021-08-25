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
    async def add_coins(self, ctx: Context, user, amount):
        # Note for *, it tells the library to put everything
        # the user types after it into message as a string.

        if ctx.message.author.id == self.tamikara_id:

            user = re.findall(r'\b\d+\b', user)
            user = str(user[0])
            print(user)
            print(type(user))
            user_mention = await self.bot.fetch_user(int(user))

            try:
                if user in self.db.index.tolist():
                    print("i exist")
                    self.db.at[user, 'bank'] += int(amount)
                    # self.db[self.db["discord_id"] == ctx.author.id]["bank"] += int(amount)
                else:
                    print("i dont exist")
                    self.db = self.db.append(pd.Series({'bank': int(amount)}, name=user))

                print(self.db)
                with open('./bot/db/filename.pickle', 'wb') as handle:
                    pickle.dump(self.db, handle)

                await ctx.send(f"{user_mention.mention} gagne {amount} coins !")


            except Exception as error:
                print(error)
        else:
            await ctx.send('not authorized')
        print("end")

