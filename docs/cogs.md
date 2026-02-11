# Cogs — Détail des commandes

## Art (`bot/cogs/Art.py`)

| Commande | Usage | Description |
|---|---|---|
| `$ascii <texte>` | `$ascii Hello` | Convertit le texte en art ASCII avec un style aléatoire |

**Dépendance** : `art`

---

## Bank (`bot/cogs/Bank.py`)

Système de monnaie virtuelle persisté dans un fichier pickle (`bot/db/filename.pickle`).

| Commande | Usage | Description |
|---|---|---|
| `$add_coins <@user> <montant>` | `$add_coins @User 100` | Ajoute/retire des coins (réservé à l'admin `ADMIN_ID`) |
| `$bank` | `$bank` | Affiche le solde de l'auteur |

**Restriction** : `$add_coins` est réservé à l'admin configuré via `ADMIN_ID`.

**Stockage** : DataFrame pandas sérialisé en pickle. Le script `script/create_pandas_df.py` permet de réinitialiser la base.

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

## Stream (`bot/cogs/Stream.py`)

Lecteur audio en vocal via YouTube.

| Commande | Usage | Description |
|---|---|---|
| `$play <url>` | `$play https://youtube.com/...` | Télécharge et joue un audio YouTube |
| `$leave` | `$leave` | Déconnecte le bot du salon vocal |
| `$pause` | `$pause` | Met l'audio en pause |
| `$resume` | `$resume` | Reprend l'audio |
| `$stop` | `$stop` | Arrête l'audio |
| `$reset` | `$reset` | Stop + supprime les fichiers mp3 + quitte le vocal |

**Dépendances** : `yt-dlp`, `PyNaCl`, `ffmpeg` (installé dans le Dockerfile)

**Fonctionnement** : Le fichier audio est téléchargé en mp3, renommé `song.mp3`, puis lu avec `FFmpegPCMAudio`.
