import pytest
import os
from unittest.mock import AsyncMock, MagicMock
from bot.cogs.Joke import Joke


@pytest.fixture
def joke_cog(bot):
    return Joke(bot)


@pytest.mark.asyncio
async def test_joke_sends_message(joke_cog, ctx):
    """Test that $joke sends a non-empty message."""
    await Joke.say_joke.callback(joke_cog, ctx)
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert len(sent_text) > 0


@pytest.mark.asyncio
async def test_joke_tts_sends_with_tts(joke_cog, ctx):
    """Test that $joke_tts sends a message with tts=True."""
    await Joke.say_joke_tts.callback(joke_cog, ctx)
    ctx.send.assert_called_once()
    kwargs = ctx.send.call_args[1]
    assert kwargs.get('tts') is True


@pytest.mark.asyncio
async def test_joke_csv_exists():
    """Test that the joke database file exists."""
    assert os.path.exists('./bot/db/joke.csv')
