import asyncio
import os
from bot import Bot

# Configuration pour VPS OVH (threads bloqués)
# Désactiver complètement l'executor par défaut
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_default_executor(None)

# Create the bot
bot = Bot()


if __name__ == '__main__':
    bot.run()