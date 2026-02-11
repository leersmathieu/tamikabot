# Configuration

| Variable d'environnement | Description | Obligatoire |
|---|---|---|
| `DISCORD_TOKEN` | Token d'authentification du bot Discord | Oui |
| `ADMIN_ID` | ID Discord de l'admin (autorisation des commandes sensibles) | Oui (pour $add_coins / $say) |
| `DISCORD_APP_ID` | ID de l'application Discord | Non (non utilisé) |

Le fichier `.env` à la racine est chargé par Docker Compose. Pour un lancement local, il faut exporter la variable manuellement.
