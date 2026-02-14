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

## Docker Compose (VPS - production)

Sur le VPS, utiliser un `docker-compose.yml` adapté (sans `build`, avec l'image Docker Hub) :

```yaml
services:
  bgutil-provider:
    image: brainicism/bgutil-ytdlp-pot-provider
    restart: unless-stopped
    init: true
    ports:
      - "4416:4416"

  tamikabot:
    image: leersma/tamikabot:latest
    restart: unless-stopped
    privileged: true
    ulimits:
      nproc: 65535
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./bot/db/:/opt/app/bot/db/
      - ./cookies.txt:/opt/app/cookies.txt:ro
    env_file:
      - .env
    depends_on:
      - bgutil-provider
```

```bash
# Pull et lancement
docker-compose pull
docker-compose up -d

# Arrêt
docker-compose down

# Logs
docker-compose logs -f
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
- Monte `./cookies.txt` pour l'authentification YouTube
- Redémarre automatiquement sauf arrêt manuel (`restart: unless-stopped`)

## Authentification YouTube (yt-dlp)

YouTube peut bloquer les requêtes yt-dlp avec l'erreur `Sign in to confirm you're not a bot`.

### PO Token (solution principale)

Le plugin **bgutil-ytdlp-pot-provider** génère automatiquement des PO Tokens (Proof of Origin) pour authentifier les requêtes. C'est la solution recommandée car elle fonctionne indépendamment de l'IP.

- Le service `bgutil-provider` tourne dans un container Docker séparé
- Le plugin Python est installé dans l'image tamikabot via `requirements.txt`
- yt-dlp communique avec le serveur via `http://bgutil-provider:4416`

Aucune configuration manuelle n'est nécessaire, tout est géré par le `docker-compose.yml`.

### Cookies YouTube (solution complémentaire)

Les cookies peuvent être utilisés en complément du PO Token :

1. Installer l'extension [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) sur Chrome
2. Se connecter à YouTube, exporter les cookies
3. Placer le fichier `cookies.txt` à la racine du projet

Le fichier est monté en read-only (`:ro`) et copié vers `/tmp/cookies.txt` au démarrage du bot pour éviter que yt-dlp ne l'écrase.

> **Note** : Les cookies sont liés à l'IP d'export. Ils fonctionnent en local mais peuvent être rejetés sur un VPS avec une IP différente. Le PO Token résout ce problème.

## Lancement local (sans Docker)

```bash
pip install -r requirements.txt
export DISCORD_TOKEN='votre_token_ici'    # Linux/Mac
set DISCORD_TOKEN=votre_token_ici         # Windows CMD
python main.py
```

**Prérequis local** : ffmpeg doit être installé et accessible dans le PATH.
