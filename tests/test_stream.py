import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from collections import deque
from bot.cogs.Stream import Stream, SongInfo


@pytest.fixture
def stream_cog(bot):
    return Stream(bot)


@pytest.fixture
def fake_song():
    return SongInfo(
        source_url="https://fake-audio-url.com/audio.webm",
        title="Test Song",
        webpage_url="https://youtube.com/watch?v=abc123",
    )


@pytest.fixture
def voice_ctx(ctx):
    """Context with author connected to a voice channel."""
    ctx.author.voice = MagicMock()
    ctx.author.voice.channel = MagicMock()
    ctx.author.voice.channel.name = "General"
    ctx.author.voice.channel.connect = AsyncMock()
    ctx.guild.id = 123456
    return ctx


# ── SongInfo ─────────────────────────────────────────────────────────

def test_song_info_from_ytdlp():
    """Test SongInfo.from_ytdlp creates a SongInfo from yt-dlp data."""
    data = {
        'url': 'https://audio.example.com/stream',
        'title': 'My Song',
        'webpage_url': 'https://youtube.com/watch?v=xyz',
    }
    song = SongInfo.from_ytdlp(data)
    assert song.source_url == data['url']
    assert song.title == data['title']
    assert song.webpage_url == data['webpage_url']


def test_song_info_from_ytdlp_missing_fields():
    """Test SongInfo.from_ytdlp handles missing fields gracefully."""
    song = SongInfo.from_ytdlp({})
    assert song.source_url == ''
    assert song.title == 'Unknown'
    assert song.webpage_url == ''


# ── play ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_play_not_in_voice(stream_cog, ctx):
    """Test that $play requires the user to be in a voice channel."""
    ctx.author.voice = None
    await Stream.play.callback(stream_cog, ctx, query="test")
    ctx.send.assert_called_with("You are not connected to a voice channel.")


@pytest.mark.asyncio
async def test_play_no_results(stream_cog, voice_ctx):
    """Test that $play handles no search results."""
    stream_cog._extract_info = MagicMock(return_value=None)
    mock_voice = MagicMock()
    mock_voice.is_connected.return_value = True
    mock_voice.is_playing.return_value = False
    mock_voice.is_paused.return_value = False
    mock_voice.channel = voice_ctx.author.voice.channel
    stream_cog.bot.voice_clients = [mock_voice]

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.play.callback(stream_cog, voice_ctx, query="nonexistent")

    voice_ctx.send.assert_any_call("No results found.")


@pytest.mark.asyncio
async def test_play_success(stream_cog, voice_ctx):
    """Test that $play streams audio successfully."""
    stream_cog._extract_info = MagicMock(return_value={
        'url': 'https://audio.example.com/stream',
        'title': 'Test Song',
        'webpage_url': 'https://youtube.com/watch?v=abc',
    })
    mock_voice = MagicMock()
    mock_voice.is_connected.return_value = True
    mock_voice.is_playing.return_value = False
    mock_voice.is_paused.return_value = False
    mock_voice.channel = voice_ctx.author.voice.channel
    stream_cog.bot.voice_clients = [mock_voice]

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.play.callback(stream_cog, voice_ctx, query="test song")

    mock_voice.play.assert_called_once()
    voice_ctx.send.assert_any_call("🎵 Now playing: **Test Song**")


@pytest.mark.asyncio
async def test_play_adds_to_queue_when_playing(stream_cog, voice_ctx):
    """Test that $play adds to queue if already playing."""
    stream_cog._extract_info = MagicMock(return_value={
        'url': 'https://audio.example.com/stream2',
        'title': 'Second Song',
        'webpage_url': 'https://youtube.com/watch?v=def',
    })
    mock_voice = MagicMock()
    mock_voice.is_connected.return_value = True
    mock_voice.is_playing.return_value = True
    mock_voice.is_paused.return_value = False
    mock_voice.channel = voice_ctx.author.voice.channel
    stream_cog.bot.voice_clients = [mock_voice]

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.play.callback(stream_cog, voice_ctx, query="second song")

    mock_voice.play.assert_not_called()
    voice_ctx.send.assert_any_call("📋 Added to queue (#1): **Second Song**")
    assert len(stream_cog._get_queue(voice_ctx.guild.id)) == 1


# ── skip ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_skip_when_playing(stream_cog, voice_ctx):
    """Test that $skip stops current audio (triggers _play_next via callback)."""
    mock_voice = MagicMock()
    mock_voice.is_playing.return_value = True

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.skip.callback(stream_cog, voice_ctx)

    mock_voice.stop.assert_called_once()
    voice_ctx.send.assert_called_with("⏭ Skipped.")


@pytest.mark.asyncio
async def test_skip_when_not_playing(stream_cog, voice_ctx):
    """Test that $skip notifies when nothing is playing."""
    mock_voice = MagicMock()
    mock_voice.is_playing.return_value = False

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.skip.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("Nothing is playing.")


# ── queue ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_queue_empty(stream_cog, voice_ctx):
    """Test that $queue shows empty message."""
    await Stream.queue.callback(stream_cog, voice_ctx)
    voice_ctx.send.assert_called_with("Queue is empty.")


@pytest.mark.asyncio
async def test_queue_with_songs(stream_cog, voice_ctx, fake_song):
    """Test that $queue displays current + queued songs."""
    guild_id = voice_ctx.guild.id
    stream_cog.current[guild_id] = fake_song
    stream_cog.queues[guild_id] = deque([
        SongInfo("url2", "Song Two", "web2"),
        SongInfo("url3", "Song Three", "web3"),
    ])

    await Stream.queue.callback(stream_cog, voice_ctx)

    sent_msg = voice_ctx.send.call_args[0][0]
    assert "Now playing:" in sent_msg
    assert "Test Song" in sent_msg
    assert "Song Two" in sent_msg
    assert "Song Three" in sent_msg


# ── leave ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_leave_connected(stream_cog, voice_ctx, fake_song):
    """Test that $leave disconnects and clears queue."""
    guild_id = voice_ctx.guild.id
    stream_cog.current[guild_id] = fake_song
    stream_cog.queues[guild_id] = deque([fake_song])

    mock_voice = MagicMock()
    mock_voice.is_connected.return_value = True
    mock_voice.disconnect = AsyncMock()

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.leave.callback(stream_cog, voice_ctx)

    mock_voice.stop.assert_called_once()
    mock_voice.cleanup.assert_called_once()
    mock_voice.disconnect.assert_awaited_once()
    assert guild_id not in stream_cog.queues
    assert guild_id not in stream_cog.current


@pytest.mark.asyncio
async def test_leave_not_connected(stream_cog, voice_ctx):
    """Test that $leave notifies when not connected."""
    with patch('discord.utils.get', return_value=None):
        await Stream.leave.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("Not connected")


# ── pause ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_pause_when_playing(stream_cog, voice_ctx):
    """Test that $pause pauses audio."""
    mock_voice = MagicMock()
    mock_voice.is_playing.return_value = True

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.pause.callback(stream_cog, voice_ctx)

    mock_voice.pause.assert_called_once()
    voice_ctx.send.assert_called_with("⏸ Paused.")


@pytest.mark.asyncio
async def test_pause_when_not_playing(stream_cog, voice_ctx):
    """Test that $pause notifies when no audio is playing."""
    mock_voice = MagicMock()
    mock_voice.is_playing.return_value = False

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.pause.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("No audio is playing")


# ── resume ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_resume_when_paused(stream_cog, voice_ctx):
    """Test that $resume resumes paused audio."""
    mock_voice = MagicMock()
    mock_voice.is_paused.return_value = True

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.resume.callback(stream_cog, voice_ctx)

    mock_voice.resume.assert_called_once()
    voice_ctx.send.assert_called_with("▶ Resumed.")


@pytest.mark.asyncio
async def test_resume_when_not_paused(stream_cog, voice_ctx):
    """Test that $resume notifies when audio is not paused."""
    mock_voice = MagicMock()
    mock_voice.is_paused.return_value = False

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.resume.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("Audio not paused")


# ── stop ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_stop_when_connected(stream_cog, voice_ctx, fake_song):
    """Test that $stop stops audio and clears queue."""
    guild_id = voice_ctx.guild.id
    stream_cog.current[guild_id] = fake_song
    stream_cog.queues[guild_id] = deque([fake_song])

    mock_voice = MagicMock()

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.stop.callback(stream_cog, voice_ctx)

    mock_voice.stop.assert_called_once()
    voice_ctx.send.assert_called_with("⏹ Stopped.")
    assert guild_id not in stream_cog.queues
    assert guild_id not in stream_cog.current


@pytest.mark.asyncio
async def test_stop_when_not_connected(stream_cog, voice_ctx):
    """Test that $stop notifies when not connected."""
    with patch('discord.utils.get', return_value=None):
        await Stream.stop.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("Not connected")


# ── reset ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_reset_when_connected(stream_cog, voice_ctx, fake_song):
    """Test that $reset stops, clears queue, and disconnects."""
    guild_id = voice_ctx.guild.id
    stream_cog.current[guild_id] = fake_song
    stream_cog.queues[guild_id] = deque([fake_song])

    mock_voice = MagicMock()
    mock_voice.disconnect = AsyncMock()

    with patch('discord.utils.get', return_value=mock_voice):
        await Stream.reset.callback(stream_cog, voice_ctx)

    mock_voice.stop.assert_called_once()
    mock_voice.cleanup.assert_called_once()
    mock_voice.disconnect.assert_awaited_once()
    voice_ctx.send.assert_called_with("🔄 Reset complete.")
    assert guild_id not in stream_cog.queues
    assert guild_id not in stream_cog.current


@pytest.mark.asyncio
async def test_reset_when_not_connected(stream_cog, voice_ctx):
    """Test that $reset notifies when not connected."""
    with patch('discord.utils.get', return_value=None):
        await Stream.reset.callback(stream_cog, voice_ctx)

    voice_ctx.send.assert_called_with("Not connected")


# ── _play_next ───────────────────────────────────────────────────────

@patch('discord.FFmpegPCMAudio')
def test_play_next_with_queue(mock_ffmpeg, stream_cog, fake_song):
    """Test that _play_next plays the next song from queue."""
    guild_id = 123456
    stream_cog.queues[guild_id] = deque([fake_song])
    mock_voice = MagicMock()

    stream_cog._play_next(guild_id, mock_voice)

    mock_voice.play.assert_called_once()
    assert stream_cog.current[guild_id] == fake_song
    assert len(stream_cog.queues[guild_id]) == 0


@patch('discord.FFmpegPCMAudio')
def test_play_next_empty_queue(mock_ffmpeg, stream_cog):
    """Test that _play_next disconnects when queue is empty."""
    import sys
    stream_module = sys.modules['bot.cogs.Stream']
    original = asyncio.run_coroutine_threadsafe
    mock_run_coro = MagicMock()
    asyncio.run_coroutine_threadsafe = mock_run_coro

    guild_id = 123456
    stream_cog.queues[guild_id] = deque()
    stream_cog.current[guild_id] = MagicMock()
    stream_cog.bot.loop = MagicMock()
    mock_voice = MagicMock()

    try:
        stream_cog._play_next(guild_id, mock_voice)
    finally:
        asyncio.run_coroutine_threadsafe = original

    mock_voice.play.assert_not_called()
    assert guild_id not in stream_cog.current
    assert guild_id not in stream_cog.queues
    mock_run_coro.assert_called_once()
