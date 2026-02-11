# Intents Discord

Le bot déclare les Intents suivants dans `bot.py` :
- **`default()`** : Intents de base (guilds, messages, reactions…)
- **`message_content`** : Accès au contenu des messages (Privileged Intent)

**Action requise** : Dans le [portail développeur Discord](https://discord.com/developers/applications), aller dans Bot > Privileged Gateway Intents et activer :
- **Message Content Intent**
