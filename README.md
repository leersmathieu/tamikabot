# TamikaBot

Bot Discord personnel écrit en Python avec `discord.py` (v2.4.0). Architecture modulaire via Cogs, conteneurisé avec Docker.

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

### 3. Lancement avec Docker Compose (recommandé)
```bash
docker-compose up -d
```

### 4. Lancement avec Docker (manuel)
```bash
docker build -t leersma/tamikabot:latest .
docker run -e DISCORD_TOKEN='VOTRE_TOKEN' -e ADMIN_ID='VOTRE_ID' -v ./bot/db/:/opt/app/bot/db/ leersma/tamikabot:latest
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

### Messages
- `$del_messages <N>` — Supprime N messages (requiert `manage_messages`)
- `$say <channel_id> <texte>` — Envoie un message (admin `ADMIN_ID`)

### Stream
- `$play <url>` — Joue une musique YouTube
- `$pause` / `$resume` / `$stop` / `$reset` / `$leave` — Contrôle audio

## Configuration requise

### Variables d'environnement
| Variable | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot | Oui |
| `ADMIN_ID` | ID Discord de l'admin (commandes sensibles) | Oui |

### Intents Discord
Activer dans le [portail développeur Discord](https://discord.com/developers/applications) → Bot → Privileged Gateway Intents :
- **Message Content Intent**

## Tests

```bash
# Via Docker (recommandé)
docker run --rm leersma/tamikabot:latest -m pytest tests/ -v

# En local
python -m pytest tests/ -v
```

Les tests couvrent tous les Cogs (sauf Stream) et la configuration du bot.

## Documentation

La documentation technique a été découpée en plusieurs fichiers dans `docs/` :
- `docs/README.md` — Sommaire
- `docs/overview.md` — Vue d'ensemble
- `docs/architecture.md` — Architecture du projet
- `docs/configuration.md` — Configuration détaillée
- `docs/cogs.md` — Détail des commandes
- `docs/deployment.md` — Déploiement (Docker)
- `docs/tests.md` — Tests
- `docs/intents.md` — Intents Discord
- `docs/notes.md` — Points d'attention

## Développement

### Prérequis locaux
- Python 3.9+
- ffmpeg (dans le PATH pour la musique)

### Installation locale
```bash
pip install -r requirements.txt
export DISCORD_TOKEN='VOTRE_TOKEN'
export ADMIN_ID='VOTRE_ID'
python main.py
```

## Historique

- **v2.x** : Migration vers `discord.py` 2.4.0, Intents, tests unitaires, documentation découpée, suppression LFG, configuration `ADMIN_ID`
- **v1.x** : Version initiale Python (migration depuis Node.js)

## Node.js Version

La version originale en Node.js est toujours disponible :
https://github.com/leersmathieu/tamikabot/tree/nodejs