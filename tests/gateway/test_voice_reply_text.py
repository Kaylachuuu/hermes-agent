"""``voice.reply_text: false``: a voice reply to a voice message goes out without the text after it."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gateway.config import Platform
from gateway.platforms.base import BasePlatformAdapter, SendResult
from gateway.run import GatewayRunner


def _adapter(platform: Platform, *, reply_text=None, success: bool = True) -> SimpleNamespace:
    adapter = SimpleNamespace(platform=platform, play_tts=AsyncMock(return_value=SendResult(success=success)))
    if reply_text is not None:
        adapter._voice_reply_text = reply_text
    return adapter


async def _play(adapter, text: str = "hello there") -> bool:
    event = SimpleNamespace(source=SimpleNamespace(chat_id="chat-1"))
    return await BasePlatformAdapter._play_tts_file(adapter, event, text, "reply.mp3", True, {}, MagicMock())


@pytest.mark.asyncio
async def test_text_still_follows_the_voice_note_by_default():
    assert await _play(_adapter(Platform("photon"))) is False                # attribute never synced
    assert await _play(_adapter(Platform("photon"), reply_text=True)) is False


@pytest.mark.asyncio
async def test_reply_text_false_skips_the_text_after_a_delivered_voice_note():
    adapter = _adapter(Platform("photon"), reply_text=False)
    assert await _play(adapter) is True
    assert adapter.play_tts.await_args.kwargs["caption"] is None             # no caption outside Telegram


@pytest.mark.asyncio
async def test_text_is_sent_when_the_voice_note_failed():
    assert await _play(_adapter(Platform("photon"), reply_text=False, success=False)) is False


@pytest.mark.asyncio
async def test_telegram_caption_behaviour_is_unchanged():
    adapter = _adapter(Platform.TELEGRAM)
    assert await _play(adapter) is True
    assert adapter.play_tts.await_args.kwargs["caption"] == "hello there"


def _runner() -> GatewayRunner:
    with patch("gateway.run.GatewayRunner._load_voice_modes", return_value={}):
        runner = GatewayRunner.__new__(GatewayRunner)
        runner._voice_mode = {}
        runner.adapters = {}
    return runner


def _syncable(platform: Platform) -> MagicMock:
    adapter = MagicMock()
    adapter.platform = platform
    adapter._auto_tts_disabled_chats, adapter._auto_tts_enabled_chats = set(), set()
    return adapter


@pytest.mark.parametrize(("voice_cfg", "expected"), [
    ({}, True),
    ({"reply_text": True}, True),
    ({"reply_text": False}, False),
    ({"reply_text": None}, True),       # only an explicit false turns the text off
])
def test_sync_copies_voice_reply_text_onto_the_adapter(voice_cfg, expected):
    adapter = _syncable(Platform.TELEGRAM)
    with patch("hermes_cli.config.load_config", return_value={"voice": voice_cfg}):
        _runner()._sync_voice_mode_state_to_adapter(adapter)
    assert adapter._voice_reply_text is expected


def test_sync_keeps_the_text_when_config_cannot_be_read():
    adapter = _syncable(Platform.TELEGRAM)
    with patch("hermes_cli.config.load_config", side_effect=OSError("unreadable")):
        _runner()._sync_voice_mode_state_to_adapter(adapter)
    assert adapter._voice_reply_text is True and adapter._auto_tts_default is False
