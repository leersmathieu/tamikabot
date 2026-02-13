# Déploiement

## Docker Hub (push des changements)

```bash
# 1. Build local avec les derniers changements
docker build -t tamikabot:latest .

# 2. Tag pour Docker Hub
docker tag tamikabot:latest leersma/tamikabot:latest

# 3. Push sur Docker Hub
docker push leersma/tamikabot:latest

# 4. Vérifier sur Docker Hub
# https://hub.docker.com/r/leersma/tamikabot
```

## Docker (VPS - production)

```bash
# Sur le VPS : pull et lancement avec l'image Docker Hub
docker pull leersma/tamikabot:latest
docker run -d --name tamikabot --restart unless-stopped \
  -e DISCORD_TOKEN='votre_token_ici' \
  -e ADMIN_ID='votre_id_admin' \
  -v /opt/tamikabot/db:/opt/app/bot/db \
  leersma/tamikabot:latest

# Arrêt
docker stop tamikabot
docker rm tamikabot

# Logs
docker logs -f tamikabot
```

## Docker Compose (développement local)

```bash
# Build local et lancement
docker-compose up -d --build

# Arrêt
docker-compose down

# Logs
docker-compose logs -f
```

### Docker Compose (local) vs Docker Hub (production)

**Développement local** :
- Utilise `docker-compose.yml` avec `build: .`
- Crée l'image locale `tamikabot:latest`
- Contient les derniers changements non publiés

**Production VPS** :
- Utilise l'image Docker Hub `leersma/tamikabot:latest`
- Plus simple à déployer, pas de build nécessaire
- Contient la dernière version publiée stable

Le `docker-compose.yml` :
- Build local `tamikabot:latest` (`build: .`)
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
