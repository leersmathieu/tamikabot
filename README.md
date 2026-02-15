# TamikaBot

Bot Discord personnel écrit en Python avec `discord.py` (v2.6.4). Architecture modulaire via Cogs, conteneurisé avec Docker.

## Démarrage rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/leersmathieu/tamikabot.git
cd tamikabot
```

### 2. Configuration
Créer un fichier `.env` à la racine :
```bash
DISCORD_TOKEN = VOTRE_TOKEN_DISCORD_ICI
ADMIN_ID = VOTRE_ID_DISCORD_ADMIN
```

### 3. Lancement (développement local)
```bash
docker build -t tamikabot:latest .
docker-compose up -d
```

### 4. Déploiement (production VPS)
```bash
# Push sur Docker Hub
docker tag tamikabot:latest leersma/tamikabot:latest
docker push leersma/tamikabot:latest

# Sur le VPS
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## Commandes disponibles

### Art
- `$ascii <texte>` — Convertit le texte en art ASCII

### Bank
- `$add_coins <@user> <montant>` — Ajoute/retire des coins (admin `ADMIN_ID`)
- `$bank` — Affiche votre solde

### Google
- `$google <recherche>` — Renvoie un lien de recherche Google
- `$translate <lang> <texte>` — Traduit le texte

### Joke
- `$joke` — Envoie une blague aléatoire
- `$joke_tts` — Blague avec text-to-speech

### Lfg (Payday2France)
- `$recherche` — Envoie un message LFG aléatoire (nécessite le rôle « Recherche joueurs »)

### Messages
- `$del_messages <N>` — Supprime N messages (requiert `manage_messages`)
- `$say <channel_id> <texte>` — Envoie un message (admin `ADMIN_ID`)

### Reminder
- `$remind <délai> <message>` — Crée un rappel (ex: `$remind 30m Lancer la lessive`)
- `$reminders` — Liste vos rappels actifs
- `$remind_cancel <id>` — Annule un rappel

### Stream
- `$play <url ou recherche>` — Joue un audio YouTube (URL ou mots-clés)
- `$skip` — Passe à la chanson suivante
- `$queue` — Affiche la queue de lecture
- `$pause` / `$resume` / `$stop` / `$reset` / `$leave` — Contrôle audio

## Configuration requise

### Variables d'environnement
| Variable | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot | Oui |
| `ADMIN_ID` | ID Discord de l'admin (commandes sensibles) | Oui |
| `DISABLED_COGS` | Cogs à désactiver, séparés par des virgules (ex: `Stream,Lfg`) | Non |

### Intents Discord
Activer dans le [portail développeur Discord](https://discord.com/developers/applications) → Bot → Privileged Gateway Intents :
- **Message Content Intent**

## Tests

```bash
# Via Docker (build local)
docker build -t tamikabot:latest .
docker run --rm tamikabot:latest -m pytest tests/ -v

# Via Docker Hub (version publiée)
docker run --rm leersma/tamikabot:latest -m pytest tests/ -v

# En local
python -m pytest tests/ -v
```

**Note** : `tamikabot:latest` est le build local (derniers changements). `leersma/tamikabot:latest` est l'image Docker Hub (version publiée).

Les tests couvrent tous les Cogs (Art, Bank, Google, Joke, Lfg, Messages, Reminder, Stream) et la configuration du bot (67 tests). Le cog Lfg est spécifique au serveur Payday2France.

## Documentation

La documentation technique complète est disponible dans `docs/` :
- **[docs/README.md](docs/README.md)** — Documentation principale (vue d'ensemble, configuration, architecture, tests)
- **[docs/cogs.md](docs/cogs.md)** — Détail de toutes les commandes par Cog
- **[docs/deployment.md](docs/deployment.md)** — Guide de déploiement Docker (local et VPS)
- **[docs/migration_sqlite.md](docs/migration_sqlite.md)** — Migration des données pickle vers SQLite
- **[docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md)** — Idées d'améliorations futures

## Développement

### Prérequis locaux
- Python 3.12+
- ffmpeg (dans le PATH pour le streaming audio)
- Node.js 20.x (pour yt-dlp signature decryption)

### Installation locale
```bash
pip install -r requirements.txt
export DISCORD_TOKEN='VOTRE_TOKEN'
export ADMIN_ID='VOTRE_ID'
python main.py
```

## Historique

- **v3.x** : Cog Reminder (rappels persistants), streaming YouTube avec PO Token (bgutil), Node.js 20.x pour yt-dlp, Python 3.12, `discord.py` 2.6.4, SQLite pour Bank et Reminder, documentation en français
- **v2.x** : Migration vers `discord.py` 2.4.0, Intents, tests unitaires, documentation découpée, configuration `ADMIN_ID`
- **v1.x** : Version initiale Python (migration depuis Node.js)

## Node.js Version

La version originale en Node.js est toujours disponible :
https://github.com/leersmathieu/tamikabot/tree/nodejs