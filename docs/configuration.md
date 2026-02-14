# Configuration

| Variable d'environnement | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot Discord | Oui |
| `ADMIN_ID` | ID Discord de l'admin (autorisation des commandes sensibles) | Oui (pour $add_coins / $say) |
| `DISCORD_APP_ID` | ID de l'application Discord | Non (non utilisé) |
| `DISABLED_COGS` | Liste de Cogs à désactiver, séparés par des virgules | Non |

Le fichier `.env` à la racine est chargé par Docker Compose. Pour un lancement local, il faut exporter les variables manuellement.

## Désactivation de Cogs

La variable `DISABLED_COGS` permet de désactiver des Cogs au démarrage du bot. Les noms doivent correspondre exactement aux clés du registre (`Messages`, `Google`, `Joke`, `Art`, `Bank`, `Stream`, `Lfg`).

Exemple dans `.env` pour désactiver Stream en production :
```
DISABLED_COGS=Stream
```

Plusieurs Cogs peuvent être désactivés :
```
DISABLED_COGS=Stream,Lfg
```

> **Note** : Le cog Lfg est spécifique au serveur Payday2France. Si vous l'utilisez sur un autre serveur, vous devrez adapter le rôle `Recherche joueurs` et les phrases dans `bot/lfg_sentences.py`.
