import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot.cogs.Lfg import Lfg, LFG_ROLE_NAME
from bot.lfg_sentences import lfg_sentences


@pytest.fixture
def lfg_cog(bot):
    return Lfg(bot)


@pytest.fixture
def lfg_ctx(ctx):
    """Context with a guild that has the LFG role."""
    role = MagicMock()
    role.name = LFG_ROLE_NAME
    ctx.guild.roles = [role]
    ctx.author.roles = [role]
    return ctx


@pytest.mark.asyncio
async def test_lfg_sends_message(lfg_cog, lfg_ctx):
    """Test that $recherche sends a message containing the author mention."""
    await Lfg.looking_for_group.callback(lfg_cog, lfg_ctx)
    lfg_ctx.send.assert_called_once()
    sent_text = lfg_ctx.send.call_args[0][0]
    assert f"<@{lfg_ctx.author.id}>" in sent_text


@pytest.mark.asyncio
async def test_lfg_no_role_on_server(lfg_cog, ctx):
    """Test that $recherche warns when the LFG role doesn't exist on the server."""
    ctx.guild.roles = []
    await Lfg.looking_for_group.callback(lfg_cog, ctx)
    ctx.send.assert_called_once()
    assert LFG_ROLE_NAME in ctx.send.call_args[0][0]
    assert "n'existe pas" in ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_lfg_user_missing_role(lfg_cog, ctx):
    """Test that $recherche warns when the user doesn't have the LFG role."""
    role = MagicMock()
    role.name = LFG_ROLE_NAME
    ctx.guild.roles = [role]
    ctx.author.roles = []  # user does NOT have the role
    await Lfg.looking_for_group.callback(lfg_cog, ctx)
    ctx.send.assert_called_once()
    assert LFG_ROLE_NAME in ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_lfg_sentence_from_list(lfg_cog, lfg_ctx):
    """Test that the sent message is derived from one of the lfg_sentences."""
    await Lfg.looking_for_group.callback(lfg_cog, lfg_ctx)
    sent_text = lfg_ctx.send.call_args[0][0]
    # The sent text should match one of the sentences with {} replaced by the mention
    mention = f"<@{lfg_ctx.author.id}>"
    possible = [s.replace("{}", mention) for s in lfg_sentences]
    assert sent_text in possible


@pytest.mark.asyncio
async def test_lfg_sentences_loaded(lfg_cog):
    """Test that the cog loads all sentences from lfg_sentences."""
    assert lfg_cog.sentences is lfg_sentences
    assert len(lfg_cog.sentences) > 0
