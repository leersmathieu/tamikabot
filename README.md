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

### Stream
- `$play <url>` — Joue une musique YouTube
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

Les tests couvrent tous les Cogs (Art, Bank, Google, Joke, Lfg, Messages, Stream) et la configuration du bot (46 tests). Le cog Lfg est spécifique au serveur Payday2France.

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
- Python 3.10+
- ffmpeg (dans le PATH pour la musique)

### Installation locale
```bash
pip install -r requirements.txt
export DISCORD_TOKEN='VOTRE_TOKEN'
export ADMIN_ID='VOTRE_ID'
python main.py
```

## Historique

- **v3.x** : Réintégration du cog LFG (Payday2France), désactivation de Cogs via `DISABLED_COGS`, streaming YouTube avec PO Token, Python 3.12, `discord.py` 2.6.4
- **v2.x** : Migration vers `discord.py` 2.4.0, Intents, tests unitaires, documentation découpée, configuration `ADMIN_ID`
- **v1.x** : Version initiale Python (migration depuis Node.js)

## Node.js Version

La version originale en Node.js est toujours disponible :
https://github.com/leersmathieu/tamikabot/tree/nodejs