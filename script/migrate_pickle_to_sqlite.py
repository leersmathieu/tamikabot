import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.db.database import BankDatabase


def migrate_pickle_to_sqlite():
    pickle_path = './bot/db/filename.pickle'
    
    if not Path(pickle_path).exists():
        print(f"Pickle file not found at {pickle_path}")
        print("Nothing to migrate. Initializing empty SQLite database...")
        db = BankDatabase()
        print(f"✅ SQLite database created at: ./bot/db/bank.db")
        return
    
    try:
        with open(pickle_path, 'rb') as handle:
            df = pickle.load(handle)
            print(f"Loaded pickle file with {len(df)} users")
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return
    
    db = BankDatabase()
    
    migrated_count = 0
    for discord_id, row in df.iterrows():
        try:
            coins = int(row['bank'])
            db.set_balance(str(discord_id), coins)
            migrated_count += 1
            print(f"Migrated user {discord_id}: {coins} coins")
        except Exception as e:
            print(f"Error migrating user {discord_id}: {e}")
    
    print(f"\n✅ Migration complete! {migrated_count}/{len(df)} users migrated successfully.")
    print(f"SQLite database created at: ./bot/db/bank.db")
    print(f"\nYou can now safely delete the old pickle file:")
    print(f"  rm {pickle_path}")


if __name__ == '__main__':
    migrate_pickle_to_sqlite()
