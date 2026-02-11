import pytest
import discord
from unittest.mock import AsyncMock, MagicMock, patch
from bot.config import Config


def test_config_loads_token_from_env():
    """Test that Config reads DISCORD_TOKEN from environment."""
    with patch.dict('os.environ', {'DISCORD_TOKEN': 'test-token-123'}):
        config = Config()
        assert config.TOKEN == 'test-token-123'


def test_config_token_none_when_missing():
    """Test that Config.TOKEN is None when env var is missing."""
    with patch.dict('os.environ', {}, clear=True):
        config = Config()
        assert config.TOKEN is None


def test_bot_has_correct_intents():
    """Test that Bot is configured with the required intents."""
    with patch.dict('os.environ', {'DISCORD_TOKEN': 'fake-token'}):
        from bot.bot import Bot
        bot = Bot()
        assert bot.intents.message_content is True


def test_bot_has_correct_prefix():
    """Test that Bot uses $ as command prefix."""
    with patch.dict('os.environ', {'DISCORD_TOKEN': 'fake-token'}):
        from bot.bot import Bot
        bot = Bot()
        assert bot.command_prefix == '$'
