import pytest
import os
import time
from unittest.mock import MagicMock, AsyncMock, patch
from bot.cogs.Reminder import Reminder
from bot.db.database import ReminderDatabase


@pytest.fixture
def reminder_db(tmp_path):
    """Create a temporary SQLite DB for testing."""
    db_path = tmp_path / "reminders.db"
    return ReminderDatabase(str(db_path))


@pytest.fixture
def reminder_cog(bot, reminder_db):
    """Create a Reminder cog instance for testing."""
    with patch.object(Reminder, '__init__', lambda self, b: None):
        cog = Reminder.__new__(Reminder)
        cog.bot = bot
        cog.db = reminder_db
        cog.check_reminders = MagicMock()
    return cog


@pytest.fixture
def ctx():
    """Create a mock context."""
    ctx = MagicMock()
    ctx.author = MagicMock()
    ctx.author.id = 123456789
    ctx.author.name = "TestUser"
    ctx.channel = MagicMock()
    ctx.channel.id = 987654321
    ctx.guild = MagicMock()
    ctx.guild.id = 111222333
    ctx.send = AsyncMock()
    return ctx


def test_parse_time_seconds(reminder_cog):
    """Test parsing seconds."""
    assert reminder_cog.parse_time("30s") == 30
    assert reminder_cog.parse_time("45S") == 45


def test_parse_time_minutes(reminder_cog):
    """Test parsing minutes."""
    assert reminder_cog.parse_time("15m") == 900
    assert reminder_cog.parse_time("30M") == 1800


def test_parse_time_hours(reminder_cog):
    """Test parsing hours."""
    assert reminder_cog.parse_time("2h") == 7200
    assert reminder_cog.parse_time("1H") == 3600


def test_parse_time_days(reminder_cog):
    """Test parsing days."""
    assert reminder_cog.parse_time("1d") == 86400
    assert reminder_cog.parse_time("7D") == 604800


def test_parse_time_invalid(reminder_cog):
    """Test invalid time formats."""
    assert reminder_cog.parse_time("invalid") is None
    assert reminder_cog.parse_time("30") is None
    assert reminder_cog.parse_time("m30") is None
    assert reminder_cog.parse_time("30x") is None


@pytest.mark.asyncio
async def test_remind_creates_reminder(reminder_cog, ctx):
    """Test that $remind creates a reminder."""
    await Reminder.remind.callback(reminder_cog, ctx, "30m", message="Test reminder")
    
    ctx.send.assert_called_once()
    args = ctx.send.call_args
    embed = args[1]['embed']
    
    assert "✅ Rappel créé" in embed.title
    assert "Test reminder" in embed.description


@pytest.mark.asyncio
async def test_remind_invalid_format(reminder_cog, ctx):
    """Test that $remind rejects invalid time format."""
    await Reminder.remind.callback(reminder_cog, ctx, "invalid", message="Test")
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "Format de temps invalide" in sent_text


@pytest.mark.asyncio
async def test_remind_too_short(reminder_cog, ctx):
    """Test that $remind rejects delays under 10 seconds."""
    await Reminder.remind.callback(reminder_cog, ctx, "5s", message="Test")
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "délai minimum" in sent_text


@pytest.mark.asyncio
async def test_remind_too_long(reminder_cog, ctx):
    """Test that $remind rejects delays over 30 days."""
    await Reminder.remind.callback(reminder_cog, ctx, "31d", message="Test")
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "délai maximum" in sent_text


@pytest.mark.asyncio
async def test_list_reminders_empty(reminder_cog, ctx):
    """Test that $reminders shows empty message when no reminders."""
    await Reminder.list_reminders.callback(reminder_cog, ctx)
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "aucun rappel actif" in sent_text


@pytest.mark.asyncio
async def test_list_reminders_with_data(reminder_cog, ctx):
    """Test that $reminders lists active reminders."""
    current_time = int(time.time())
    reminder_cog.db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    await Reminder.list_reminders.callback(reminder_cog, ctx)
    
    ctx.send.assert_called_once()
    args = ctx.send.call_args
    embed = args[1]['embed']
    
    assert "Vos rappels actifs" in embed.title
    assert len(embed.fields) == 1
    assert "Test reminder" in embed.fields[0].value


@pytest.mark.asyncio
async def test_cancel_reminder_success(reminder_cog, ctx):
    """Test that $remind_cancel cancels a reminder."""
    current_time = int(time.time())
    reminder_id = reminder_cog.db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    await Reminder.cancel_reminder.callback(reminder_cog, ctx, reminder_id)
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "annulé" in sent_text


@pytest.mark.asyncio
async def test_cancel_reminder_not_found(reminder_cog, ctx):
    """Test that $remind_cancel handles non-existent reminder."""
    await Reminder.cancel_reminder.callback(reminder_cog, ctx, 999)
    
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert "introuvable" in sent_text


def test_database_add_reminder(reminder_db):
    """Test adding a reminder to database."""
    current_time = int(time.time())
    reminder_id = reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    assert reminder_id > 0


def test_database_get_pending_reminders(reminder_db):
    """Test getting pending reminders."""
    current_time = int(time.time())
    
    reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Past reminder",
        remind_at=current_time - 100,
        created_at=current_time - 200
    )
    
    reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Future reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    pending = reminder_db.get_pending_reminders(current_time)
    assert len(pending) == 1
    assert pending[0][4] == "Past reminder"


def test_database_mark_completed(reminder_db):
    """Test marking a reminder as completed."""
    current_time = int(time.time())
    reminder_id = reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    reminder_db.mark_completed(reminder_id)
    
    pending = reminder_db.get_pending_reminders(current_time + 7200)
    assert len(pending) == 0


def test_database_get_user_reminders(reminder_db):
    """Test getting user's reminders."""
    current_time = int(time.time())
    
    reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="User 1 reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    reminder_db.add_reminder(
        user_id="987654321",
        channel_id="987654321",
        guild_id="111222333",
        message="User 2 reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    user_reminders = reminder_db.get_user_reminders("123456789")
    assert len(user_reminders) == 1
    assert user_reminders[0][1] == "User 1 reminder"


def test_database_delete_reminder(reminder_db):
    """Test deleting a reminder."""
    current_time = int(time.time())
    reminder_id = reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    result = reminder_db.delete_reminder(reminder_id, "123456789")
    assert result is True
    
    user_reminders = reminder_db.get_user_reminders("123456789")
    assert len(user_reminders) == 0


def test_database_delete_wrong_user(reminder_db):
    """Test that users can only delete their own reminders."""
    current_time = int(time.time())
    reminder_id = reminder_db.add_reminder(
        user_id="123456789",
        channel_id="987654321",
        guild_id="111222333",
        message="Test reminder",
        remind_at=current_time + 3600,
        created_at=current_time
    )
    
    result = reminder_db.delete_reminder(reminder_id, "999999999")
    assert result is False
    
    user_reminders = reminder_db.get_user_reminders("123456789")
    assert len(user_reminders) == 1
