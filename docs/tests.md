# Tests

Les tests unitaires couvrent tous les Cogs (sauf Stream) et la configuration du bot (20 tests au total).

```bash
# Via Docker (recommandé)
docker run --rm leersma/tamikabot:latest -m pytest tests/ -v

# En local
python -m pytest tests/ -v
```

Les tests utilisent `unittest.mock` pour simuler le bot et le contexte Discord. En discord.py 2.x, les commandes sont des descripteurs `Command` — les callbacks sont appelés via `CogClass.method.callback(cog_instance, ctx, ...)`.
