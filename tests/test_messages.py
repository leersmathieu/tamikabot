import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.cogs.Messages import Messages
import os


@pytest.fixture
def messages_cog(bot):
    return Messages(bot)


@pytest.mark.asyncio
async def test_say_denied_for_non_admin(messages_cog, ctx):
    """Test that $say is restricted to tamikara_id."""
    ctx.message.author.id = 111111111
    ctx.message.author.bot = False
    mock_channel = MagicMock()
    mock_channel.send = AsyncMock()
    messages_cog.bot.get_channel.return_value = mock_channel

    await Messages.say.callback(messages_cog, ctx, chan_id=123456, text="hello")
    # Non-admin should not trigger channel.send
    mock_channel.send.assert_not_called()


@pytest.mark.asyncio
async def test_say_allowed_for_admin(messages_cog, ctx):
    """Test that $say works for tamikara_id."""
    ctx.message.author.id = int(os.environ['ADMIN_ID'])
    ctx.message.author.bot = False
    ctx.message.author == messages_cog.bot.user  # not the bot
    mock_channel = MagicMock()
    mock_channel.send = AsyncMock()
    messages_cog.bot.get_channel.return_value = mock_channel
    messages_cog.bot.user = MagicMock()
    messages_cog.bot.user.id = 999999999

    await Messages.say.callback(messages_cog, ctx, chan_id=123456, text="hello")
    mock_channel.send.assert_called_once_with("hello")


@pytest.mark.asyncio
async def test_delete_messages_denied_without_permission(messages_cog, ctx):
    """Test that $del_messages requires manage_messages permission."""
    ctx.message.author.guild_permissions.manage_messages = False
    await Messages.delete_messages.callback(messages_cog, ctx, number_of_messages=5)
    ctx.send.assert_called_once_with('Permission denied!')
