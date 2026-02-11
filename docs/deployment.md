# Déploiement

## Docker (recommandé)

```bash
# Build de l'image
docker build -t leersma/tamikabot:latest .

# Lancement
docker run -e DISCORD_TOKEN='votre_token_ici' -v ./bot/db/:/opt/app/bot/db/ leersma/tamikabot:latest
```

## Docker Compose (recommandé)

```bash
# Build de l'image
docker build -t leersma/tamikabot:latest .

# Lancement
docker-compose up -d

# Arrêt
docker-compose down

# Logs
docker-compose logs -f
```

Le `docker-compose.yml` :
- Utilise l'image `leersma/tamikabot:latest`
- Charge le token depuis le fichier `.env` via `env_file`
- Monte `./bot/db/` pour persister la base Bank
- Redémarre automatiquement sauf arrêt manuel (`restart: unless-stopped`)

## Lancement local (sans Docker)

```bash
pip install -r requirements.txt
export DISCORD_TOKEN='votre_token_ici'    # Linux/Mac
set DISCORD_TOKEN=votre_token_ici         # Windows CMD
python main.py
```

**Prérequis local** : ffmpeg doit être installé et accessible dans le PATH.
