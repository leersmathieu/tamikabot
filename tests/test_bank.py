import pytest
import os
from unittest.mock import patch
from bot.cogs.Bank import Bank
from bot.db.database import BankDatabase


@pytest.fixture
def bank_db(tmp_path):
    """Create a temporary SQLite DB for testing."""
    db_path = tmp_path / "bank.db"
    db = BankDatabase(str(db_path))
    admin_id = os.environ.get('ADMIN_ID', '183999045168005120')
    db.set_balance(admin_id, 100)
    return db


@pytest.fixture
def bank_cog(bot, bank_db):
    with patch.object(Bank, '__init__', lambda self, b: None):
        cog = Bank.__new__(Bank)
        cog.bot = bot
        cog.admin_id = int(os.environ.get('ADMIN_ID', '183999045168005120'))
        cog.db = bank_db
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


@pytest.mark.asyncio
async def test_add_coins_creates_new_account(bank_cog, ctx, bot):
    """Test that $add_coins creates a new account if it doesn't exist."""
    ctx.message.author.id = int(os.environ['ADMIN_ID'])
    bot.fetch_user.return_value.mention = "<@123456789>"
    
    await Bank.add_coins.callback(bank_cog, ctx, "<@123456789>", 50)
    
    balance = bank_cog.db.get_balance("123456789")
    assert balance == 50
    ctx.send.assert_called_once()


@pytest.mark.asyncio
async def test_add_coins_updates_existing_account(bank_cog, ctx, bot):
    """Test that $add_coins updates an existing account."""
    admin_id = os.environ['ADMIN_ID']
    ctx.message.author.id = int(admin_id)
    bot.fetch_user.return_value.mention = f"<@{admin_id}>"
    
    await Bank.add_coins.callback(bank_cog, ctx, f"<@{admin_id}>", 50)
    
    balance = bank_cog.db.get_balance(admin_id)
    assert balance == 150
    ctx.send.assert_called_once()


@pytest.mark.asyncio
async def test_add_coins_removes_coins(bank_cog, ctx, bot):
    """Test that $add_coins can remove coins with negative amount."""
    admin_id = os.environ['ADMIN_ID']
    ctx.message.author.id = int(admin_id)
    bot.fetch_user.return_value.mention = f"<@{admin_id}>"
    
    await Bank.add_coins.callback(bank_cog, ctx, f"<@{admin_id}>", -30)
    
    balance = bank_cog.db.get_balance(admin_id)
    assert balance == 70
    ctx.send.assert_called_once()
