# TamikaBot — Améliorations & Idées de features
 
## Améliorations techniques prioritaires
 
### ~~1. Migration vers discord.py 2.x~~ ✅

**Réalisé.** Migration de discord.py 1.7.3 vers 2.4.0 :
- Intents explicites (`message_content`)
- `add_cog()` asynchrone via `setup_hook()`
- `pass_context=True` supprimé de toutes les commandes
- `history().flatten()` remplacé par `[m async for m in channel.history()]`
- Tests unitaires ajoutés (20 tests, tous passent)

**Note** : Les slash commands (`/`) ne sont pas encore implémentés. Les commandes restent en prefix `$`. La migration vers les slash commands est une évolution future possible.
 
---
 
### ~~2. Gestion des Intents~~ ✅

**Réalisé.** Intents configurés dans `bot.py` :
```python
intents = discord.Intents.default()
intents.message_content = True
```
**Action restante** : Activer "Message Content Intent" dans le portail développeur Discord (Bot > Privileged Gateway Intents).
 
---
 
### 3. Remplacement du stockage pickle par SQLite
 
**Pourquoi** : Le fichier pickle est fragile (corruption en cas de crash pendant l'écriture), non lisible manuellement, et pose des risques de sécurité (exécution de code arbitraire à la désérialisation).
 
**Solution** : Remplacer par `sqlite3` (inclus dans Python, zéro dépendance). Un simple fichier `bank.db` avec une table `users(discord_id TEXT PRIMARY KEY, coins INTEGER)`.
 
**Bénéfice** : Transactions atomiques, requêtes SQL, pas de dépendance à pandas juste pour la Bank.
 
---
 
### 4. Remplacement de googletrans
 
**Pourquoi** : `googletrans==4.0.0rc1` est une release candidate qui utilise l'API non officielle de Google Translate. Elle casse régulièrement quand Google change ses endpoints.
 
**Alternatives** :
- **`deep-translator`** — wrapper stable multi-moteurs (Google, DeepL, MyMemory…)
- **API DeepL gratuite** — 500k caractères/mois gratuits, bien plus fiable
 
---
 
### 5. Stream cog : streaming audio sans téléchargement
 
**Pourquoi** : Actuellement le bot télécharge le MP3 sur disque avant de le lire. C'est lent et consomme de l'espace.
 
**Solution** : Utiliser `yt-dlp` pour extraire l'URL du stream audio et la passer directement à `FFmpegPCMAudio` :
```python
ffmpeg_opts = {'options': '-vn'}
source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_opts)
```
Cela supprime le temps de téléchargement et la gestion des fichiers temporaires.
 
---
 
### 6. Centraliser la configuration des IDs
 
**Pourquoi** : L'ID admin (`tamikara_id = 183999045168005120`) est dupliqué dans `Bank.py` et `Messages.py`.
 
**Solution** : Tout centraliser dans `config.py` via des variables d'environnement :
```
ADMIN_ID=183999045168005120
```
 
---
 
### 7. Gestion d'erreurs globale
 
**Pourquoi** : Beaucoup de `try/except` avec des `print(error)` silencieux. En production (Docker), ces erreurs sont difficilement traçables.
 
**Solution** : Utiliser le logger partout (déjà initialisé dans certains fichiers) et enrichir le `on_command_error` dans `events.py` pour gérer plus de cas (commande inconnue, mauvais arguments, permissions manquantes…).
 
---
 
## Idées de features
 
### 1. Système de rappels / Reminders
 
Un système de rappels personnels via le bot :
```
$remind 30m Lancer la lessive
$remind 2h Rejoindre le raid
```
 
**Fonctionnement** :
- L'utilisateur crée un rappel avec un délai ou une heure précise
- Le bot envoie un DM ou un message dans le canal à l'heure prévue
- Utilisation de `discord.ext.tasks` pour les boucles de vérification ou `asyncio.sleep` pour les rappels simples
 
**Intérêt** : Feature utile au quotidien, simple à implémenter, pas de dépendance externe. Persistance possible avec SQLite (survit aux redémarrages).
 
---
 
### 2. Dashboard de présence / Activité du serveur
 
Un système qui track l'activité vocale et textuelle des membres :
- Temps passé en vocal par semaine
- Nombre de messages envoyés
- Commande `$stats` ou `$stats @user` pour afficher un résumé
- Commande `$leaderboard` pour un classement hebdo
 
**Fonctionnement** :
- Listener `on_voice_state_update` pour tracker les connexions/déconnexions vocales
- Incrémenter un compteur dans SQLite à chaque message via `on_message`
- Générer un embed Discord formaté avec les stats
 
**Intérêt** : Donne de la vie au serveur, encourage l'activité, et c'est le type de feature que les bots publics font payer en premium.
 
 # Points d'attention

- **googletrans 4.0.0rc1** est une version release candidate qui peut être instable car elle dépend de l'API non officielle de Google Translate.
- **Persistance Bank** : Le fichier pickle n'est pas robuste (corruption possible). Aucun backup n'est en place.
