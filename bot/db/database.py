import sqlite3
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class BankDatabase:
    def __init__(self, db_path: str = './bot/db/bank.db'):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()

    def _ensure_db_directory(self):
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    discord_id TEXT PRIMARY KEY,
                    coins INTEGER NOT NULL DEFAULT 0
                )
            ''')
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    def get_balance(self, discord_id: str) -> Optional[int]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT coins FROM users WHERE discord_id = ?', (discord_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def add_coins(self, discord_id: str, amount: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (discord_id, coins)
                VALUES (?, ?)
                ON CONFLICT(discord_id) DO UPDATE SET coins = coins + ?
            ''', (discord_id, amount, amount))
            conn.commit()
            
            cursor.execute('SELECT coins FROM users WHERE discord_id = ?', (discord_id,))
            return cursor.fetchone()[0]

    def set_balance(self, discord_id: str, amount: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (discord_id, coins)
                VALUES (?, ?)
                ON CONFLICT(discord_id) DO UPDATE SET coins = ?
            ''', (discord_id, amount, amount))
            conn.commit()
            return amount

    def user_exists(self, discord_id: str) -> bool:
        return self.get_balance(discord_id) is not None
