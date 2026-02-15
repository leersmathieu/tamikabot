# TamikaBot — Améliorations & Idées de features
 
## Améliorations techniques prioritaires
 
 
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
 
### ~~1. Système de rappels / Reminders~~ ✅

**Réalisé.** Système de rappels personnels avec persistance SQLite :
- Commandes : `$remind <délai> <message>`, `$reminders`, `$remind_cancel <id>`
- Formats de délai : `30s`, `15m`, `2h`, `7d` (min: 10s, max: 30j)
- Base de données SQLite (`bot/db/reminders.db`) avec persistance complète
- Notifications par DM ou mention dans le canal si DMs fermés
- Vérification automatique toutes les 30 secondes via `discord.ext.tasks`
- Tests unitaires complets (20 tests)

**Bénéfices** : Feature utile au quotidien, zéro dépendance externe, survit aux redémarrages du bot.
 
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
 
---

### 3. Système de paris entre membres

Un mini-jeu de paris entre utilisateurs du serveur :
```
$bet @user 100 Je finis avant toi
$bet accept
$bet winner @user
```

**Fonctionnement** :
- Un membre crée un pari avec une mise en coins (lié à la Bank)
- L'autre membre accepte ou refuse
- Un admin ou les deux joueurs désignent le gagnant
- Les coins sont transférés automatiquement

**Intérêt** : Crée de l'interaction sociale, réutilise le système Bank existant, très fun en vocal pendant les games.

---

### 4. Soundboard — Sons courts en vocal

Une soundboard pour jouer des sons courts (airhorn, sad trombone, applause…) :
```
$sb airhorn
$sb list
$sb add nom_du_son <attachment>
```

**Fonctionnement** :
- Fichiers audio courts stockés dans `bot/sounds/`
- Le bot rejoint le vocal, joue le son, et se déconnecte (ou reste si de la musique tourne)
- Les membres peuvent ajouter leurs propres sons (avec une limite de durée ~5s)

**Intérêt** : Feature classique des bots fun, très utilisée en vocal pendant les sessions de jeu. Complémentaire au Stream cog.

---

### 5. Système de roulette / Mini-casino

Des mini-jeux de casino utilisant les coins de la Bank :
```
$roulette 50 red
$slots 100
$coinflip 200
$daily
```

**Fonctionnement** :
- `$roulette` : mise sur rouge/noir/numéro, multiplicateur classique
- `$slots` : machine à sous avec emojis, combinaisons gagnantes
- `$coinflip` : pile ou face, x2 la mise
- `$daily` : bonus quotidien de coins pour encourager l'activité

**Intérêt** : Donne un vrai usage aux coins de la Bank, très addictif, facile à implémenter. Pas de dépendance externe (juste `random`).

---

### 6. Système de citations / Quotes

Sauvegarder les meilleures citations du serveur :
```
$quote add @user "Je suis pas bourré, je suis juste fatigué horizontalement"
$quote random
$quote list @user
$quote top
```

**Fonctionnement** :
- Stockage dans SQLite (auteur, citation, date, nombre de likes)
- `$quote random` pour ressortir une pépite au hasard
- Réaction 👍 pour voter sur les citations
- `$quote top` pour le hall of fame

**Intérêt** : Feature très communautaire, crée des inside jokes, donne envie de revenir sur le serveur. Zéro dépendance externe.

---

### 7. Polls avancés avec réactions

Un système de sondages interactifs :
```
$poll "On joue à quoi ce soir ?" "Valorant" "CS2" "Rocket League" "Rien je suis claqué"
```

**Fonctionnement** :
- Le bot crée un embed avec les options numérotées
- Ajoute automatiquement les réactions 1️⃣ 2️⃣ 3️⃣ 4️⃣
- Timer optionnel (`$poll 30m "Question" ...`) avec résultat automatique
- Affiche les résultats en pourcentage à la fin

**Intérêt** : Remplace les sondages manuels, visuellement propre avec les embeds, utile au quotidien.

---

 # Points d'attention

- **googletrans 4.0.0rc1** est une version release candidate qui peut être instable car elle dépend de l'API non officielle de Google Translate.
