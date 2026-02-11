import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.cogs.Google import Google


@pytest.fixture
def google_cog(bot):
    return Google(bot)


@pytest.mark.asyncio
async def test_google_search_returns_url(google_cog, ctx):
    """Test that $google returns a valid Google search URL."""
    await Google.google_search.callback(google_cog, ctx, entry="python discord bot")
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert sent_text.startswith("https://www.google.com/search?q=")


@pytest.mark.asyncio
async def test_google_search_encodes_special_chars(google_cog, ctx):
    """Test that special characters are URL-encoded."""
    await Google.google_search.callback(google_cog, ctx, entry="hello world")
    sent_text = ctx.send.call_args[0][0]
    # Space should be encoded as %20 or +
    assert "hello" in sent_text
    assert " " not in sent_text.split("?q=")[1]
