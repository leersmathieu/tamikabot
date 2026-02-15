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
# Build l'image manuellement
docker build -t tamikabot:latest .

# Lancement
docker-compose up -d

# Arrêt
docker-compose down

# Logs
docker-compose logs -f
```

### Local vs Production

| | Développement local | Production VPS |
|---|---|---|
| **Fichier** | `docker-compose.yml` | `docker-compose.prod.yml` |
| **Image** | `tamikabot:latest` (build local) | `leersma/tamikabot:latest` (Docker Hub) |
| **Build** | Manuel (`docker build`) | Aucun (pull depuis Docker Hub) |

Les deux fichiers incluent le service `bgutil-provider` pour l'authentification YouTube (PO Token).

## Désactivation de Cogs

Pour désactiver un ou plusieurs Cogs (par exemple Stream en production), ajouter dans le `.env` :

```
DISABLED_COGS=Stream
```

Voir `docs/README.md` (section Configuration) pour plus de détails.

> **Note** : Le cog Lfg est spécifique au serveur Payday2France. Si vous l'utilisez sur un autre serveur, vous devrez adapter le rôle `Recherche joueurs` et les phrases dans `bot/lfg_sentences.py`.

## Authentification YouTube (yt-dlp)

YouTube peut bloquer les requêtes yt-dlp avec l'erreur `Sign in to confirm you're not a bot`.

### PO Token (solution principale)

Le plugin **bgutil-ytdlp-pot-provider** génère automatiquement des PO Tokens (Proof of Origin) pour authentifier les requêtes. C'est la solution recommandée car elle fonctionne indépendamment de l'IP.

- Le service `bgutil-provider` tourne dans un container Docker séparé
- Le plugin est installé dans le répertoire des plugins yt-dlp (`/root/.config/yt-dlp/plugins`) via le Dockerfile
- yt-dlp communique avec le serveur via `http://bgutil-provider:4416`
- La configuration de l'extracteur est définie dans `Stream.py` avec `extractor_args`

Aucune configuration manuelle n'est nécessaire, tout est géré par le `docker-compose.yml` et le Dockerfile.

### Cookies YouTube (solution complémentaire)

Les cookies peuvent être utilisés en complément du PO Token :

1. Installer l'extension [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) sur Chrome
2. Se connecter à YouTube, exporter les cookies
3. Placer le fichier `cookies.txt` à la racine du projet

Le fichier est monté en read-only (`:ro`) et copié vers `/tmp/cookies.txt` au démarrage du bot pour éviter que yt-dlp ne l'écrase.

> **Note** : Les cookies sont liés à l'IP d'export. Ils fonctionnent en local mais peuvent être rejetés sur un VPS avec une IP différente. Le PO Token résout ce problème.

## Dépannage YouTube / yt-dlp

### Erreur "Sign in to confirm you're not a bot"

Si vous obtenez cette erreur malgré la présence du plugin bgutil et des cookies :

**1. Vérifier que les cookies sont valides**

Les cookies YouTube expirent régulièrement (rotation de sécurité). Le message d'erreur suivant dans les logs indique des cookies expirés :

```
WARNING: [youtube] The provided YouTube account cookies are no longer valid
```

**Solution** : Réexporter les cookies depuis votre navigateur :
1. Connectez-vous à YouTube dans votre navigateur
2. Utilisez l'extension [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
3. Exportez les cookies et remplacez le fichier `cookies.txt` à la racine du projet
4. Redémarrez les containers : `docker compose restart`

**2. Vérifier que le plugin bgutil fonctionne**

Activez temporairement le mode verbose dans `bot/cogs/Stream.py` :

```python
YDL_OPTIONS = {
    'quiet': False,
    'verbose': True,
    # ... reste de la config
}
```

Recherchez dans les logs :
- `[debug] Plugin directories:` → confirme que les plugins sont chargés
- `[pot] PO Token Providers: bgutil:http-1.2.2 (external)` → confirme que bgutil est détecté
- `Generating a gvs PO Token for ... client via bgutil HTTP server` → confirme que bgutil génère des tokens

**3. Vérifier la connectivité réseau**

Le container `tamikabot` doit pouvoir atteindre `bgutil-provider:4416`. Testez depuis le container :

```bash
docker exec tamikabot-tamikabot-1 wget -O- http://bgutil-provider:4416/ping
```

Vous devriez obtenir une réponse JSON avec la version du serveur.

## Lancement local (sans Docker)

```bash
pip install -r requirements.txt
export DISCORD_TOKEN='votre_token_ici'    # Linux/Mac
set DISCORD_TOKEN=votre_token_ici         # Windows CMD
python main.py
```

**Prérequis locaux** : 
- Python 3.12+
- ffmpeg (dans le PATH pour le streaming audio)
- Node.js 20.x (pour yt-dlp signature decryption)
- bgutil-ytdlp-pot-provider doit être lancé séparément ou désactiver le cog Stream
