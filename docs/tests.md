# Tests

Les tests unitaires couvrent tous les Cogs (Art, Bank, Google, Joke, Lfg, Messages, Stream) et la configuration du bot (46 tests). Le cog Lfg est spécifique au serveur Payday2France.

```bash
# Via Docker (build local)
docker build -t tamikabot:latest .
docker run --rm tamikabot:latest -m pytest tests/ -v

# Via Docker Hub (version publiée)
docker run --rm leersma/tamikabot:latest -m pytest tests/ -v

# En local (Python 3.10+)
python -m pytest tests/ -v
```

**Note** : Pour le développement local, utilisez `tamikabot:latest` (build local). L'image `leersma/tamikabot:latest` sur Docker Hub contient la dernière version publiée et peut ne pas inclure les derniers changements.

Les tests utilisent `unittest.mock` pour simuler le bot et le contexte Discord. En discord.py 2.x, les commandes sont des descripteurs `Command` — les callbacks sont appelés via `CogClass.method.callback(cog_instance, ctx, ...)`.
