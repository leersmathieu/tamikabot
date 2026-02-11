import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.cogs.Art import Art


@pytest.fixture
def art_cog(bot):
    return Art(bot)


@pytest.mark.asyncio
async def test_ascii_returns_code_block(art_cog, ctx):
    """Test that $ascii wraps output in a code block."""
    await Art.ascii.callback(art_cog, ctx, sentences="Hi")
    ctx.send.assert_called_once()
    sent_text = ctx.send.call_args[0][0]
    assert sent_text.startswith("```")
    assert sent_text.endswith("```")


@pytest.mark.asyncio
async def test_ascii_contains_text(art_cog, ctx):
    """Test that the ASCII art contains recognizable characters (non-empty)."""
    await Art.ascii.callback(art_cog, ctx, sentences="AB")
    sent_text = ctx.send.call_args[0][0]
    # Strip the code block markers and check it's not empty
    inner = sent_text.strip("`").strip()
    assert len(inner) > 0
