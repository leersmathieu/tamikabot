# Migration pickle vers SQLite

## Contexte

Le système Bank utilisait auparavant un fichier pickle (`bot/db/filename.pickle`) pour stocker les données des utilisateurs. Ce système présentait plusieurs problèmes :
- **Risque de corruption** : En cas de crash pendant l'écriture, le fichier pouvait être corrompu
- **Sécurité** : Le pickle peut exécuter du code arbitraire lors de la désérialisation
- **Lisibilité** : Format binaire non lisible manuellement
- **Couplage fort** : Nécessitait pandas pour la gestion du stockage

## Solution implémentée

Migration vers SQLite avec les avantages suivants :
- **Transactions atomiques** : Garanties par SQLite, pas de corruption possible
- **Sécurité** : Pas d'exécution de code arbitraire
- **Lisibilité** : Format SQL standard, lisible avec n'importe quel client SQLite
- **Découplage** : `sqlite3` est inclus dans Python, pas de dépendance externe pour le stockage

**Note importante** : Pandas est conservé dans `requirements.txt` car il est utilisé par :
- Le script de migration `migrate_pickle_to_sqlite.py` (pour lire l'ancien fichier pickle)
- Le script utilitaire `create_pandas_df.py` (pour créer des fichiers pickle de test)
- Le script `check_versions.py` (pour vérifier les versions des dépendances)

Le cog Bank n'utilise plus pandas et repose uniquement sur SQLite.

## Structure de la base de données

```sql
CREATE TABLE users (
    discord_id TEXT PRIMARY KEY,
    coins INTEGER NOT NULL DEFAULT 0
)
```

## Fichiers modifiés

### Nouveaux fichiers
- `bot/db/database.py` : Module de gestion de la base de données SQLite
- `bot/db/__init__.py` : Export du module BankDatabase
- `script/migrate_pickle_to_sqlite.py` : Script de migration des données existantes
- `docs/migration_sqlite.md` : Cette documentation

### Fichiers modifiés
- `bot/cogs/Bank.py` : Utilise maintenant `BankDatabase` (SQLite) au lieu de pickle/pandas
- `bot/cogs/Joke.py` : Refactorisé pour utiliser le module `csv` standard au lieu de pandas
- `tests/test_bank.py` : Tests mis à jour pour SQLite (5 tests)
- `requirements.txt` : pandas conservé (nécessaire pour scripts utilitaires et migration)
- `.gitignore` : Ajout de `bank.db` et `filename.pickle`
- `docs/architecture.md` : Documentation mise à jour
- `docs/cogs.md` : Documentation mise à jour
- `docs/IMPROVEMENTS.md` : Point 3 marqué comme réalisé

## Migration des données existantes

Si vous avez des données existantes dans `bot/db/filename.pickle`, exécutez le script de migration.

### Avec Docker (recommandé)

```bash
# Build l'image avec les nouveaux changements
docker build -t tamikabot:latest .

# Exécuter le script de migration
docker run --rm -v ./bot/db:/opt/app/bot/db tamikabot:latest script/migrate_pickle_to_sqlite.py
```

### PowerShell (Windows)

```powershell
# Build l'image
docker build -t tamikabot:latest .

# Exécuter le script de migration
docker run --rm -v ./bot/db:/opt/app/bot/db tamikabot:latest script/migrate_pickle_to_sqlite.py
```

### Sans Docker (développement local)

```bash
python script/migrate_pickle_to_sqlite.py
```

### Option alternative : Démarrer avec une base vide

Si vous n'avez pas de données à migrer ou souhaitez repartir de zéro :

```bash
# Supprimer l'ancien fichier pickle
rm bot/db/filename.pickle

# Le bot créera automatiquement une base SQLite vide au démarrage
docker-compose up -d
```

### Résultat de la migration

Le script va :
1. Charger le fichier pickle existant
2. Créer la base SQLite `bot/db/bank.db`
3. Migrer tous les utilisateurs et leurs soldes
4. Afficher un rapport de migration

**Note** : Le fichier pickle original n'est pas supprimé automatiquement. Vous pouvez le conserver comme backup ou le supprimer manuellement après vérification.

**Important** : Grâce au volume Docker (`./bot/db/:/opt/app/bot/db/`), la base de données SQLite est persistée sur l'hôte et survit aux redémarrages du container.

## Utilisation

### Dans le code

```python
from bot.db.database import BankDatabase

# Initialisation
db = BankDatabase()  # Crée automatiquement bot/db/bank.db

# Récupérer le solde d'un utilisateur
balance = db.get_balance("123456789")  # Retourne None si l'utilisateur n'existe pas

# Ajouter des coins (ou retirer si négatif)
new_balance = db.add_coins("123456789", 100)  # Retourne le nouveau solde

# Définir un solde exact
db.set_balance("123456789", 500)

# Vérifier si un utilisateur existe
exists = db.user_exists("123456789")
```

### Commandes Discord

Les commandes restent identiques :
- `$bank` : Affiche votre solde
- `$add_coins <@user> <montant>` : Ajoute/retire des coins (admin uniquement)

## Tests

Les tests unitaires ont été mis à jour pour SQLite. Pour les exécuter :

### Avec Docker (recommandé)

```bash
# Build l'image
docker build -t tamikabot:latest .

# Exécuter tous les tests
docker run --rm tamikabot:latest -m pytest tests/test_bank.py -v

# Exécuter tous les tests du projet
docker run --rm tamikabot:latest -m pytest tests/ -v
```

### Sans Docker (développement local)

```bash
# Tous les tests Bank
pytest tests/test_bank.py -v

# Test spécifique
pytest tests/test_bank.py::test_bank_shows_balance -v
```

6 tests sont disponibles :
- `test_bank_shows_balance` : Affichage du solde
- `test_bank_no_account` : Gestion des comptes inexistants
- `test_add_coins_creates_new_account` : Création de nouveau compte
- `test_add_coins_updates_existing_account` : Mise à jour de compte existant
- `test_add_coins_removes_coins` : Retrait de coins (montant négatif)

## Avantages de la migration

1. **Robustesse** : Transactions atomiques, pas de corruption
2. **Sécurité** : Pas d'exécution de code arbitraire
3. **Performance** : Requêtes SQL optimisées
4. **Maintenance** : Format standard, outils existants (DB Browser for SQLite, etc.)
5. **Simplicité** : Moins de dépendances (pandas supprimé)
6. **Évolutivité** : Facile d'ajouter de nouvelles colonnes ou tables

## Déploiement Docker

### Développement local

```bash
# 1. Build l'image avec les changements
docker build -t tamikabot:latest .

# 2. (Optionnel) Migrer les données pickle si nécessaire
docker run --rm -v ./bot/db:/opt/app/bot/db tamikabot:latest script/migrate_pickle_to_sqlite.py

# 3. Lancer le bot
docker-compose up -d

# 4. Vérifier les logs
docker-compose logs -f tamikabot
```

### Production (VPS)

```bash
# 1. Build et push sur Docker Hub
docker build -t tamikabot:latest .
docker tag tamikabot:latest leersma/tamikabot:latest
docker push leersma/tamikabot:latest

# 2. Sur le VPS - Pull la nouvelle image
docker-compose -f docker-compose.prod.yml pull

# 3. (Optionnel) Migrer les données pickle si nécessaire
docker run --rm -v ./bot/db:/opt/app/bot/db leersma/tamikabot:latest script/migrate_pickle_to_sqlite.py

# 4. Redémarrer le bot
docker-compose -f docker-compose.prod.yml up -d

# 5. Vérifier les logs
docker-compose -f docker-compose.prod.yml logs -f tamikabot
```

**Note importante** : Le volume `./bot/db/:/opt/app/bot/db/` dans `docker-compose.yml` assure la persistance de la base SQLite sur l'hôte. Les données survivent aux redémarrages et mises à jour du container.

## Compatibilité

- Python 3.12 (Dockerfile basé sur `python:3.12-slim-bookworm`)
- sqlite3 inclus dans Python (zéro dépendance externe)
- Compatible Docker sans modification des fichiers de configuration
- Volume Docker pour persistance automatique
