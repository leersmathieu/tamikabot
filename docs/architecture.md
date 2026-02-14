# Architecture

```
 tamikabot/
 ├── main.py                  # Point d'entrée — instancie et lance le bot
 ├── requirements.txt         # Dépendances Python
 ├── Dockerfile               # Image Docker (Python 3.12-bookworm + ffmpeg)
 ├── docker-compose.yml       # Orchestration Docker (développement local)
 ├── docker-compose.prod.yml  # Orchestration Docker (production VPS)
 ├── .env                     # Token Discord (non versionné)
 ├── check_versions.py        # Script utilitaire de vérification des dépendances
 ├── bot/
 │   ├── __init__.py          # Exporte Bot, Config, Events
 │   ├── bot.py               # Classe Bot principale (hérite de commands.Bot)
 │   ├── config.py            # Chargement de la configuration via variables d'environnement
 │   ├── events.py            # Événements globaux (on_ready, on_command_error)
 │   ├── lfg_sentences.py     # Phrases LFG aléatoires pour le cog Lfg (Payday2France)
 │   ├── cogs/
 │   │   ├── __init__.py      # Exporte tous les Cogs
 │   │   ├── Art.py           # Commande $ascii
 │   │   ├── Bank.py          # Commandes $bank, $add_coins
 │   │   ├── Google.py        # Commandes $google, $translate
 │   │   ├── Joke.py          # Commandes $joke, $joke_tts
 │   │   ├── Lfg.py           # Commande $recherche (Looking For Group, Payday2France)
 │   │   ├── Messages.py      # Commandes $del_messages, $say
 │   │   └── Stream.py        # Commandes $play, $skip, $queue, $leave, $pause, $resume, $stop, $reset
 │   └── db/
 │       ├── filename.pickle  # Base de données Bank (DataFrame pandas sérialisé)
 │       └── joke.csv         # Base de blagues encodées en base64
 ├── tests/                   # Tests unitaires (pytest + pytest-asyncio)
 │   ├── conftest.py          # Fixtures partagées (mock bot, mock ctx)
 │   ├── test_art.py          # Tests Art cog
 │   ├── test_bank.py         # Tests Bank cog
 │   ├── test_bot.py          # Tests Config et Bot (intents, prefix)
 │   ├── test_google.py       # Tests Google cog
 │   ├── test_joke.py         # Tests Joke cog
 │   ├── test_lfg.py          # Tests Lfg cog
 │   ├── test_messages.py     # Tests Messages cog
 │   └── test_stream.py       # Tests Stream cog
 └── script/
     └── create_pandas_df.py  # Script pour initialiser le fichier pickle de la Bank
```

## Flux d'exécution

1. `main.py` instancie `Bot()` et appelle `bot.run()`
2. `Bot.__init__()` :
   - Configure les **Intents** Discord (`message_content`)
   - Définit le préfixe `$`
   - Charge le token depuis les variables d'environnement via `Config`
3. `Bot.setup_hook()` (appelé automatiquement par discord.py avant la connexion au gateway) :
   - Enregistre tous les Cogs de manière asynchrone (sauf ceux listés dans `DISABLED_COGS`)
4. `Bot.run()` appelle `super().run(self.token)` pour connecter le bot à Discord
5. `on_message()` est déclenché à chaque message reçu → log + dispatch vers `process_commands()`
