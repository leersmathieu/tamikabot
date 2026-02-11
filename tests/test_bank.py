import pytest
import pickle
import pandas as pd
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch
from bot.cogs.Bank import Bank


@pytest.fixture
def bank_db(tmp_path):
    """Create a temporary pickle DB for testing."""
    admin_id = os.environ.get('ADMIN_ID', '183999045168005120')
    df = pd.DataFrame({'bank': [100]}, index=[admin_id])
    db_path = tmp_path / "filename.pickle"
    with open(db_path, 'wb') as f:
        pickle.dump(df, f)
    return str(db_path)


@pytest.fixture
def bank_cog(bot, bank_db):
    with patch.object(Bank, '__init__', lambda self, b: None):
        cog = Bank.__new__(Bank)
        cog.bot = bot
        cog.admin_id = int(os.environ.get('ADMIN_ID', '183999045168005120'))
        with open(bank_db, 'rb') as f:
            cog.db = pickle.load(f)
    return cog


@pytest.mark.asyncio
async def test_bank_shows_balance(bank_cog, ctx):
    """Test that $bank shows the user's balance."""
    ctx.author.id = int(os.environ['ADMIN_ID'])
    await Bank.bank.callback(bank_cog, ctx)
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "100" in sent_text


@pytest.mark.asyncio
async def test_bank_no_account(bank_cog, ctx):
    """Test that $bank shows error for unknown user."""
    ctx.author.id = 999999999
    await Bank.bank.callback(bank_cog, ctx)
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "pas de compte" in sent_text


def test_bank_pickle_file_exists():
    """Test that the bank database file exists."""
    assert os.path.exists('./bot/db/filename.pickle')
