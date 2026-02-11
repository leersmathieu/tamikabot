import sys
import os
import pytest
import discord
import asyncio
from unittest.mock import AsyncMock, MagicMock, PropertyMock
from discord.ext import commands

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def bot():
    """Create a mock bot instance."""
    os.environ.setdefault('ADMIN_ID', '183999045168005120')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    mock_bot = MagicMock(spec=commands.Bot)
    mock_bot.user = MagicMock()
    mock_bot.user.id = 999999999
    mock_bot.fetch_user = AsyncMock()
    mock_bot.get_channel = MagicMock()
    mock_bot.voice_clients = []
    return mock_bot


@pytest.fixture
def ctx():
    """Create a mock Context."""
    mock_ctx = MagicMock(spec=commands.Context)
    mock_ctx.send = AsyncMock()
    mock_ctx.author = MagicMock()
    mock_ctx.author.id = 183999045168005120
    mock_ctx.author.name = "TestUser"
    mock_ctx.author.bot = False
    mock_ctx.author.voice = None
    mock_ctx.message = MagicMock()
    mock_ctx.message.author = mock_ctx.author
    mock_ctx.message.author.guild_permissions = MagicMock()
    mock_ctx.message.author.guild_permissions.manage_messages = True
    mock_ctx.message.author.roles = []
    mock_ctx.guild = MagicMock()
    mock_ctx.guild.roles = []
    mock_ctx.channel = MagicMock()
    return mock_ctx
