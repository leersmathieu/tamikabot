# TamikaBot — Documentation technique

## Vue d'ensemble

TamikaBot est un bot Discord personnel écrit en Python avec la bibliothèque `discord.py` (v1.7.3). Il utilise le système de **prefix commands** (préfixe `$`) et une architecture modulaire basée sur les **Cogs** de discord.py. Le bot est conteneurisé avec Docker.

Originellement écrit en Node.js, il a été réécrit en Python.

---

## Architecture

```
tamikabot/
├── main.py                  # Point d'entrée — instancie et lance le bot
├── requirements.txt         # Dépendances Python
├── Dockerfile               # Image Docker (Python 3.9 + ffmpeg)
├── docker-compose.yml       # Orchestration Docker
├── .env                     # Token Discord (non versionné)
├── check_versions.py        # Script utilitaire de vérification des dépendances
├── bot/
│   ├── __init__.py          # Exporte Bot, Config, Events
│   ├── bot.py               # Classe Bot principale (hérite de commands.Bot)
│   ├── config.py            # Chargement de la configuration via variables d'environnement
│   ├── events.py            # Événements globaux (on_ready, on_command_error)
│   ├── lfg_sentences.py     # Liste de phrases pour le système LFG (Looking For Group)
│   ├── cogs/
│   │   ├── __init__.py      # Exporte tous les Cogs
│   │   ├── Art.py           # Commande $ascii
│   │   ├── Bank.py          # Commandes $bank, $add_coins
│   │   ├── Google.py        # Commandes $google, $translate
│   │   ├── Joke.py          # Commandes $joke, $joke_tts
│   │   ├── Lfg.py           # Commande $recherche (LFG Payday2france)
│   │   ├── Messages.py      # Commandes $del_messages, $say
│   │   └── Stream.py        # Commandes $play, $leave, $pause, $resume, $stop, $reset
│   └── db/
│       ├── filename.pickle  # Base de données Bank (DataFrame pandas sérialisé)
│       └── joke.csv         # Base de blagues encodées en base64
└── script/
    └── create_pandas_df.py  # Script pour initialiser le fichier pickle de la Bank
```

---

## Flux d'exécution

1. `main.py` instancie `Bot()` et appelle `bot.run()`
2. `Bot.__init__()` :
   - Définit le préfixe `$`
   - Charge le token depuis les variables d'environnement via `Config`
   - Enregistre tous les Cogs (Messages, Google, Joke, Art, Bank, Lfg, Stream)
   - Enregistre les événements globaux (Events)
3. `Bot.run()` appelle `super().run(self.token)` pour connecter le bot à Discord
4. `on_message()` est déclenché à chaque message reçu → log + dispatch vers `process_commands()`

---

## Configuration

| Variable d'environnement | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot Discord | Oui |
| `DISCORD_APP_ID` | ID de l'application Discord | Non (non utilisé) |

Le fichier `.env` à la racine est chargé par Docker Compose. Pour un lancement local, il faut exporter la variable manuellement.

---

## Cogs — Détail des commandes

### Art (`bot/cogs/Art.py`)

| Commande | Usage | Description |
|---|---|---|
| `$ascii <texte>` | `$ascii Hello` | Convertit le texte en art ASCII avec un style aléatoire |

**Dépendance** : `art`

---

### Bank (`bot/cogs/Bank.py`)

Système de monnaie virtuelle persisté dans un fichier pickle (`bot/db/filename.pickle`).

| Commande | Usage | Description |
|---|---|---|
| `$add_coins <@user> <montant>` | `$add_coins @User 100` | Ajoute/retire des coins (réservé à tamikara_id) |
| `$bank` | `$bank` | Affiche le solde de l'auteur |

**Restriction** : `$add_coins` est verrouillé à l'ID Discord `183999045168005120` (tamikara).

**Stockage** : DataFrame pandas sérialisé en pickle. Le script `script/create_pandas_df.py` permet de réinitialiser la base.

---

### Google (`bot/cogs/Google.py`)

| Commande | Usage | Description |
|---|---|---|
| `$google <recherche>` | `$google python discord bot` | Renvoie un lien de recherche Google |
| `$translate <lang> <texte>` | `$translate en Bonjour` | Traduit le texte vers la langue cible |

**Dépendance** : `googletrans==4.0.0rc1` (version RC, potentiellement instable)

---

### Joke (`bot/cogs/Joke.py`)

| Commande | Usage | Description |
|---|---|---|
| `$joke` | `$joke` | Envoie une blague aléatoire depuis la base CSV |
| `$joke_tts` | `$joke_tts` | Idem avec text-to-speech activé |

**Source** : `bot/db/joke.csv` — blagues encodées en base64, séparées par espace.

---

### Lfg (`bot/cogs/Lfg.py`)

Système "Looking For Group" pour le serveur Payday2france.

| Commande | Usage | Description |
|---|---|---|
| `$recherche` | `$recherche` | Ping le rôle "Recherche joueurs" avec une phrase aléatoire |

**Cooldown** : 1 utilisation toutes les 2700 secondes (45 min), global.

**Prérequis** : L'auteur doit posséder le rôle "Recherche joueurs". Les phrases sont définies dans `bot/lfg_sentences.py` et mentionnent un rôle Discord hardcodé (`@&973556338275799120`).

---

### Messages (`bot/cogs/Messages.py`)

| Commande | Usage | Description |
|---|---|---|
| `$del_messages <N>` | `$del_messages 10` | Supprime N messages du canal (requiert la permission `manage_messages`) |
| `$say <channel_id> <texte>` | `$say 123456789 Hello!` | Envoie un message dans un canal spécifique (réservé à tamikara_id) |

---

### Stream (`bot/cogs/Stream.py`)

Lecteur audio en vocal via YouTube.

| Commande | Usage | Description |
|---|---|---|
| `$play <url>` | `$play https://youtube.com/...` | Télécharge et joue un audio YouTube |
| `$leave` | `$leave` | Déconnecte le bot du salon vocal |
| `$pause` | `$pause` | Met l'audio en pause |
| `$resume` | `$resume` | Reprend l'audio |
| `$stop` | `$stop` | Arrête l'audio |
| `$reset` | `$reset` | Stop + supprime les fichiers mp3 + quitte le vocal |

**Dépendances** : `yt-dlp`, `PyNaCl`, `ffmpeg` (installé dans le Dockerfile)

**Fonctionnement** : Le fichier audio est téléchargé en mp3, renommé `song.mp3`, puis lu avec `FFmpegPCMAudio`.

---

## Événements globaux (`bot/events.py`)

- **`on_ready`** : Log "Ready!" quand le bot est connecté
- **`on_command_error`** : Gère le cooldown (renvoie un message avec le temps restant)

---

## Déploiement

### Docker (recommandé)

```bash
# Build de l'image
docker build -t leersma/tamikabot:latest .

# Lancement
docker run -e DISCORD_TOKEN='votre_token_ici' -v ./bot/db/:/opt/app/bot/db/ leersma/tamikabot:latest
```

### Docker Compose

Le `docker-compose.yml` utilise l'image `leersma/tamikabot:latest` depuis le registre Docker Hub.
Le volume `./bot/db/` est monté pour persister la base Bank.

**Important** : Le token dans le docker-compose actuel est un exemple/ancien token. Remplacez-le ou utilisez le `.env`.

### CI/CD

Le fichier `.travis.yml` est configuré pour builder et pusher l'image Docker sur Docker Hub à chaque push sur `main`.

### Lancement local (sans Docker)

```bash
pip install -r requirements.txt
export DISCORD_TOKEN='votre_token_ici'    # Linux/Mac
set DISCORD_TOKEN=votre_token_ici         # Windows CMD
python main.py
```

**Prérequis local** : ffmpeg doit être installé et accessible dans le PATH.

---

## Dépendances

| Package | Version | Usage |
|---|---|---|
| `discord.py` | 1.7.3 | Framework Discord bot |
| `pandas` | 2.2.2 | Gestion de la base Bank |
| `art` | 6.2 | Art ASCII |
| `googletrans` | 4.0.0rc1 | Traduction Google |
| `requests` | 2.32.3 | Requêtes HTTP |
| `PyNaCl` | 1.5.0 | Chiffrement vocal Discord |
| `yt-dlp` | 2024.12.6 | Téléchargement audio YouTube |

---

## Points d'attention

- **discord.py 1.7.3** est une version ancienne et non maintenue. La bibliothèque a été abandonnée puis reprise. Les versions modernes (2.x+) ont des breaking changes significatifs (Intents obligatoires, slash commands, etc.).
- **googletrans 4.0.0rc1** est une version release candidate qui peut être instable car elle dépend de l'API non officielle de Google Translate.
- **Persistance Bank** : Le fichier pickle n'est pas robuste (corruption possible). Aucun backup n'est en place.
- **IDs hardcodés** : L'ID `tamikara_id` (183999045168005120) et l'ID du rôle LFG (973556338275799120) sont en dur dans le code.
- **Intents** : Le bot ne déclare pas d'Intents explicitement. Discord requiert maintenant les Privileged Intents dans le portail développeur.
