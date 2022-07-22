from collections import defaultdict

from discord.ext import commands
from discord.message import Message

from .cogs import Google
from .cogs import Art
from .cogs import Joke
from .cogs import Bank
from .cogs import Stream
from .cogs import Messages
from .cogs import Lfg
from .config import Config
from .events import Events

import logging

logging.basicConfig(level=logging.INFO)

config = Config()

# database = Database(config.DB_HOST, config.DB_PASSWORD)

lfg_sentences = [
    "Appel à toutes les stations, code <@&973556338275799120>, {} est sur place !",
    "{} a allumé le bat-signal. Répondrez-vous à l’appel, <@&973556338275799120> ?",
    "C’est l’heure du braco ! {} convoque tous les <@&973556338275799120> disponibles.",
    "{} vous invoque, <@&973556338275799120> !",
    "{} a besoin de partenaires de jeu. Rejoignez sa partie, <@&973556338275799120> !",
    "Avis à la <@&973556338275799120>, {} a besoin de vous, là, maintenant !",
    "{} souhaite jouer en bonne compagnie, <@&973556338275799120> !",
    "Qui a besoin la <@&973556338275799120> ? Mais oui, c’est {} !",
    "{} cherche des coéquipiers, vous n’allez quand même pas l’ignorer, <@&973556338275799120> ?",
    "Vous cherchez une partie, <@&973556338275799120> ? Ça tombe bien, {} aussi !",
    "{} vous attend sagement dans son salon vocal pour jouer, <@&973556338275799120> !",
    "Discret, bourrin ou les deux, arrangez-vous avec {}, <@&973556338275799120>.",
    "C’est une belle journée pour jouer à plusieurs, <@&973556338275799120> ! {} vous appelle.",
    "Duo, trio ou plus, {} veut jouer à tout sauf en solo ! <@&973556338275799120>",
    "{} n’aime pas les Pubs, et c’est compréhensible. Venez donc, <@&973556338275799120> !",
    "<@&973556338275799120>. C’était juste pour vous pinger pour rien. Mais non, je blague, {} veut jouer !",
    "Embarquez dans une folle aventure criminelle avec {}, <@&973556338275799120> !",
    "Qui veut faire sauter des casques avec {}, <@&973556338275799120> ?",
    "Accompagnez donc {} dans sa croisade contre les flics de Washington, <@&973556338275799120>.",
    "Farm de succès, tryhard, chill... Rayez les mentions inutiles avec {}, <@&973556338275799120> !",
    "Les <@&973556338275799120> sont demandés à l’accueil. {} cherche des coéquipiers.",
    "{} vous ping pour la bonne cause, <@&973556338275799120>, venez jouer !",
    "PAYDAY 2 est souvent meilleur à plusieurs. C’est l’avis de {}, <@&973556338275799120> !",
    "{} a besoin d’aide pour quelques missions, vous avez un peu de temps à lui accorder, <@&973556338275799120> ?",
    "{} a hâte de tester son build avec vous, <@&973556338275799120> !",
    "Qu’est-ce qu’un jeu coop sans coopération ? {} vous lance un appel, <@&973556338275799120> !",
    "Venez ajouter vos compétences à celles de {} pour faire face à toutes les situations, <@&973556338275799120> !",
    "{} requiert poliment votre assistance pour le larcin de moult objets précieux, <@&973556338275799120>.",
    "{} cherche des potes pas peureux pour plomber des poulets, <@&973556338275799120>.",
    "Y a un peu trop de flics dans ces contrats et {} vous demande de l’aider à y remédier, <@&973556338275799120>.",
    "Tous les gens cools jouent avec {}. Enfin, c’est ce qu’on dit. Venez vérifier cette rumeur, <@&973556338275799120>.",
    "<@&973556338275799120>, si vous lisez ce message, vous devez rejoindre la partie de {} ! Désolé, c’est la loi.",
    "{} utilise <@&973556338275799120> ! Sera-t-elle super efficace ?",
    "{} vous invite à jouer, <@&973556338275799120> ! Qui sait, vous apprendrez peut-être quelque chose !",
    "Le prochain casse s’annonce peut-être coriace, {} a besoin d’une équipe, <@&973556338275799120> !",
    "Allez, rejoignez la partie, ou {} va être super triste. Bon, peut-être pas, mais venez quand même, <@&973556338275799120> !",
    "Le train vers Bracoville va partir et {} sera votre commandant de bord. En voiture, <@&973556338275799120> !",
    "{} a bien raison d’utiliser la fonction <@&973556338275799120>, c’est simple, rapide et efficace ! Venez jouer !",
    "Quelques braquages avec {}, ça vous tente, <@&973556338275799120> ?",
    "Si vous n’avez pas eu votre quota de condés dézingués, {} vous invite à y remédier, <@&973556338275799120> !",
    "Venez dropper votre skin du jour avec {}, et plus si affinités, <@&973556338275799120> !",
    "{} a besoin d’aide ! Entre braqueurs, l’entraide est primordiale, <@&973556338275799120> !",
    "Attrapez votre meilleur flingue et venez jouer, <@&973556338275799120>, ça fera très plaisir à {} !",
    "Il y a encore trop de Cloakers sans balle dans la tête. Rejoignez {} pour réparer cette injustice, <@&973556338275799120>.",
    "<@&973556338275799120>. C’est pas moi, c’est {}. Mais puisque vous êtes là, rejoignez sa partie !"
]

# Doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
class Bot(commands.Bot):

    def __init__(self):
        commands_prefixes = ['$']
    
        super().__init__(commands_prefixes)

        self.token = config.TOKEN
        self.history = defaultdict(lambda: False)

        # Register all Cogs
        self.add_cog(Messages(self))
        self.add_cog(Google(self))
        self.add_cog(Joke(self))
        self.add_cog(Art(self))
        self.add_cog(Bank(self))
        self.add_cog(Lfg(self, lfg_sentences))
        self.add_cog(Stream(self))
        
        # Register personnal events
        self.add_cog(Events(self))

    def run(self):
        """
        Override the run method to pass the token directly from self.token.
        """

        # Connect the bot to Discord servers
        super(Bot, self).run(self.token)

    # async def on_message(self, message):
    #     """
    #     Triggered when a message is send on any channel/server that the
    #     bot have access.
    #     """

    #     # Don't respond to ourselves
    #     if message.author == self.user:
    #         return

    #     # Don't respond to any bot
    #     if message.author.bot:
    #         return
        
    #     print(message)

