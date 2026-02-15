# Cogs — Détail des commandes

## Art (`bot/cogs/Art.py`)

| Commande | Usage | Description |
|---|---|---|
| `$ascii <texte>` | `$ascii Hello` | Convertit le texte en art ASCII avec un style aléatoire |

**Dépendance** : `art`

---

## Bank (`bot/cogs/Bank.py`)

Système de monnaie virtuelle persisté dans une base de données SQLite (`bot/db/bank.db`).

| Commande | Usage | Description |
|---|---|---|
| `$add_coins <@user> <montant>` | `$add_coins @User 100` | Ajoute/retire des coins (réservé à l'admin `ADMIN_ID`) |
| `$bank` | `$bank` | Affiche le solde de l'auteur |

**Restriction** : `$add_coins` est réservé à l'admin configuré via `ADMIN_ID`.

**Stockage** : Base de données SQLite avec transactions atomiques. Le script `script/migrate_pickle_to_sqlite.py` permet de migrer les anciennes données pickle.

---

## Google (`bot/cogs/Google.py`)

| Commande | Usage | Description |
|---|---|---|
| `$google <recherche>` | `$google python discord bot` | Renvoie un lien de recherche Google |
| `$translate <lang> <texte>` | `$translate en Bonjour` | Traduit le texte vers la langue cible |

**Dépendance** : `googletrans==4.0.0rc1` (version RC, potentiellement instable)

---

## Joke (`bot/cogs/Joke.py`)

| Commande | Usage | Description |
|---|---|---|
| `$joke` | `$joke` | Envoie une blague aléatoire depuis la base CSV |
| `$joke_tts` | `$joke_tts` | Idem avec text-to-speech activé |

**Source** : `bot/db/joke.csv` — blagues encodées en base64, séparées par espace.

---

## Messages (`bot/cogs/Messages.py`)

| Commande | Usage | Description |
|---|---|---|
| `$del_messages <N>` | `$del_messages 10` | Supprime N messages du canal (requiert la permission `manage_messages`) |
| `$say <channel_id> <texte>` | `$say 123456789 Hello!` | Envoie un message dans un canal spécifique (réservé à l'admin `ADMIN_ID`) |

---

## Lfg (`bot/cogs/Lfg.py`)

Système de recherche de groupe (Looking For Group) conçu spécifiquement pour le serveur **Payday2France** Discord.

| Commande | Usage | Description |
|---|---|---|
| `$recherche` | `$recherche` | Envoie un message LFG aléatoire mentionnant l'auteur et le rôle configuré |

**Restriction** : L'auteur doit posséder le rôle `Recherche joueurs` sur le serveur.

**Cooldown** : 45 minutes (global) pour éviter le spam.

**Phrases** : Les messages sont définis dans `bot/lfg_sentences.py` — chaque phrase contient un placeholder `{}` remplacé par la mention de l'auteur.

> **Note** : Ce cog est optimisé pour le serveur Payday2France. Les phrases et le rôle `Recherche joueurs` sont spécifiques à ce serveur.

---

## Stream (`bot/cogs/Stream.py`)

Lecteur audio en streaming depuis YouTube avec système de queue.

| Commande | Usage | Description |
|---|---|---|
| `$play <url ou recherche>` | `$play https://youtube.com/...` ou `$play lofi chill` | Streame un audio YouTube (URL ou recherche par mots-clés). Ajoute à la queue si déjà en lecture. |
| `$skip` | `$skip` | Passe à la chanson suivante dans la queue |
| `$queue` | `$queue` | Affiche la chanson en cours et la queue de lecture |
| `$leave` | `$leave` | Déconnecte le bot du salon vocal et vide la queue |
| `$pause` | `$pause` | Met l'audio en pause |
| `$resume` | `$resume` | Reprend l'audio |
| `$stop` | `$stop` | Arrête l'audio et vide la queue |
| `$reset` | `$reset` | Stop + vide la queue + quitte le vocal |

**Dépendances** : `yt-dlp`, `PyNaCl`, `ffmpeg` (installé dans le Dockerfile)

**Fonctionnement** : L'URL audio est extraite via `yt-dlp` (sans téléchargement) puis streamée directement avec `FFmpegPCMAudio` et des options de reconnexion automatique. Un système de queue par guild permet d'enchaîner les morceaux automatiquement.
