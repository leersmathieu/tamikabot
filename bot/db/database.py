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


class ReminderDatabase:
    def __init__(self, db_path: str = './bot/db/reminders.db'):
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
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    guild_id TEXT,
                    message TEXT NOT NULL,
                    remind_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL,
                    completed INTEGER DEFAULT 0
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_remind_at 
                ON reminders(remind_at, completed)
            ''')
            conn.commit()
            logger.info(f"Reminder database initialized at {self.db_path}")

    def add_reminder(self, user_id: str, channel_id: str, guild_id: Optional[str], 
                     message: str, remind_at: int, created_at: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reminders (user_id, channel_id, guild_id, message, remind_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, channel_id, guild_id, message, remind_at, created_at))
            conn.commit()
            return cursor.lastrowid

    def get_pending_reminders(self, current_time: int) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, channel_id, guild_id, message, remind_at
                FROM reminders
                WHERE remind_at <= ? AND completed = 0
                ORDER BY remind_at ASC
            ''', (current_time,))
            return cursor.fetchall()

    def mark_completed(self, reminder_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reminders SET completed = 1 WHERE id = ?
            ''', (reminder_id,))
            conn.commit()

    def get_user_reminders(self, user_id: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, message, remind_at, created_at
                FROM reminders
                WHERE user_id = ? AND completed = 0
                ORDER BY remind_at ASC
            ''', (user_id,))
            return cursor.fetchall()

    def delete_reminder(self, reminder_id: int, user_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM reminders WHERE id = ? AND user_id = ? AND completed = 0
            ''', (reminder_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
