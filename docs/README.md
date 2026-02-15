# TamikaBot - Documentation

## Vue d'ensemble

TamikaBot est un bot Discord personnel écrit en Python avec la bibliothèque `discord.py` (v2.6.4). Il utilise le système de **prefix commands** (préfixe `$`) et une architecture modulaire basée sur les **Cogs** de discord.py.

Originellement écrit en Node.js, il a été réécrit en Python. Les Cogs peuvent être activés/désactivés individuellement via la variable d'environnement `DISABLED_COGS`. Le cog Lfg est spécifique au serveur Payday2France.

## Configuration

| Variable d'environnement | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot Discord | Oui |
| `ADMIN_ID` | ID Discord de l'admin (autorisation des commandes sensibles) | Oui (pour $add_coins / $say) |
| `DISCORD_APP_ID` | ID de l'application Discord | Non (non utilisé) |
| `DISABLED_COGS` | Liste de Cogs à désactiver, séparés par des virgules | Non |

Le fichier `.env` à la racine est chargé par Docker Compose. Pour un lancement local, il faut exporter les variables manuellement.

### Désactivation de Cogs

La variable `DISABLED_COGS` permet de désactiver des Cogs au démarrage du bot. Les noms doivent correspondre exactement aux clés du registre (`Messages`, `Google`, `Joke`, `Art`, `Bank`, `Stream`, `Lfg`, `Reminder`).

Exemple dans `.env` pour désactiver Stream en production :
```
DISABLED_COGS=Stream
```

Plusieurs Cogs peuvent être désactivés :
```
DISABLED_COGS=Stream,Lfg
```

> **Note** : Le cog Lfg est spécifique au serveur Payday2France. Si vous l'utilisez sur un autre serveur, vous devrez adapter le rôle `Recherche joueurs` et les phrases dans `bot/lfg_sentences.py`.

## Intents Discord

Le bot déclare les Intents suivants dans `bot.py` :
- **`default()`** : Intents de base (guilds, messages, reactions…)
- **`message_content`** : Accès au contenu des messages (Privileged Intent)

**Action requise** : Dans le [portail développeur Discord](https://discord.com/developers/applications), aller dans Bot > Privileged Gateway Intents et activer :
- **Message Content Intent**

## Événements globaux (`bot/events.py`)

- **`on_ready`** : Log "Ready!" quand le bot est connecté
- **`on_message`** : Log les messages et dispatch vers `process_commands()`
- **`on_command_error`** : Gère le cooldown (renvoie un message avec le temps restant)

## Architecture

```
 tamikabot/
 ├── main.py                  # Point d'entrée — instancie et lance le bot
 ├── requirements.txt         # Dépendances Python
 ├── Dockerfile               # Image Docker (Python 3.12-bookworm + ffmpeg + Node.js 20)
 ├── docker-compose.yml       # Orchestration Docker (développement local)
 ├── docker-compose.prod.yml  # Orchestration Docker (production VPS)
 ├── .env                     # Token Discord (non versionné)
 ├── cookies.txt              # Cookies YouTube pour yt-dlp (non versionné)
 ├── check_versions.py        # Script utilitaire de vérification des dépendances
 ├── bot/
 │   ├── __init__.py          # Exporte Bot, Config, Events
 │   ├── bot.py               # Classe Bot principale (hérite de commands.Bot)
 │   ├── config.py            # Chargement de la configuration via variables d'environnement
 │   ├── events.py            # Événements globaux (on_ready, on_message, on_command_error)
 │   ├── lfg_sentences.py     # Phrases LFG aléatoires pour le cog Lfg (Payday2France)
 │   ├── cogs/
 │   │   ├── __init__.py      # Exporte tous les Cogs
 │   │   ├── Art.py           # Commande $ascii
 │   │   ├── Bank.py          # Commandes $bank, $add_coins
 │   │   ├── Google.py        # Commandes $google, $translate
 │   │   ├── Joke.py          # Commandes $joke, $joke_tts
 │   │   ├── Lfg.py           # Commande $recherche (Looking For Group, Payday2France)
 │   │   ├── Messages.py      # Commandes $del_messages, $say
 │   │   ├── Reminder.py      # Commandes $remind, $reminders, $remind_cancel
 │   │   └── Stream.py        # Commandes $play, $skip, $queue, $leave, $pause, $resume, $stop, $reset
 │   └── db/
 │       ├── database.py      # Module de gestion de la base de données SQLite (Bank + Reminder)
 │       ├── bank.db          # Base de données Bank (SQLite)
 │       ├── reminders.db     # Base de données Reminders (SQLite)
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
 │   ├── test_reminder.py     # Tests Reminder cog
 │   └── test_stream.py       # Tests Stream cog
 ├── docs/                    # Documentation
 │   ├── README.md            # Ce fichier (documentation principale)
 │   ├── cogs.md              # Détail des commandes par Cog
 │   ├── deployment.md        # Guide de déploiement Docker
 │   ├── migration_sqlite.md  # Migration pickle → SQLite
 │   └── IMPROVEMENTS.md      # Idées d'améliorations futures
 └── script/
     └── create_pandas_df.py  # Script pour initialiser le fichier pickle de la Bank (obsolète)
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

## Tests

Les tests unitaires couvrent tous les Cogs (Art, Bank, Google, Joke, Lfg, Messages, Reminder, Stream) et la configuration du bot (46+ tests).

```bash
# Via Docker (build local)
docker build -t tamikabot:latest .
docker run --rm tamikabot:latest -m pytest tests/ -v

# Via Docker Hub (version publiée)
docker run --rm leersma/tamikabot:latest -m pytest tests/ -v

# En local (Python 3.12+)
python -m pytest tests/ -v
```

**Note** : Pour le développement local, utilisez `tamikabot:latest` (build local). L'image `leersma/tamikabot:latest` sur Docker Hub contient la dernière version publiée et peut ne pas inclure les derniers changements.

Les tests utilisent `unittest.mock` pour simuler le bot et le contexte Discord. En discord.py 2.x, les commandes sont des descripteurs `Command` — les callbacks sont appelés via `CogClass.method.callback(cog_instance, ctx, ...)`.

## Voir aussi

- [Détail des commandes par Cog](cogs.md)
- [Guide de déploiement](deployment.md)
- [Migration SQLite](migration_sqlite.md)
- [Améliorations futures](IMPROVEMENTS.md)
