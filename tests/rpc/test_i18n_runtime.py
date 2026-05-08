import pytest

from freqtrade.i18n import (
    get_default_language,
    get_user_language,
    normalize_language,
    set_user_language,
    translate,
)
from freqtrade.rpc.api_server.api_schemas import StatusMsg


def test_translate_fallback_and_interpolation():
    assert translate("telegram.status_prefix", "vi") == "Trang thai"
    assert translate("telegram.status_prefix", "en") == "Status"
    # unknown locale falls back to en
    assert translate("telegram.status_prefix", "de") == "Status"
    # unknown key falls back to key itself
    assert translate("non.existing.key", "vi") == "non.existing.key"
    assert translate("telegram.command.lang.updated", "en", language="vi") == "Language updated to `vi`."


@pytest.mark.usefixtures("init_persistence")
def test_user_language_preferences_persist():
    cfg = {"telegram": {"language": "en"}, "api_server": {"default_language": "en"}}
    assert get_user_language("alice", cfg) == "en"
    assert set_user_language("alice", "vi") == "vi"
    assert get_user_language("alice", cfg) == "vi"
    assert get_user_language("bob", cfg) == "en"


def test_language_normalization_and_default_config():
    cfg = {"telegram": {"language": "vi"}, "api_server": {"default_language": "en"}}
    assert normalize_language("VI") == "vi"
    assert normalize_language("unknown") == "en"
    assert get_default_language(cfg) == "vi"


def test_statusmsg_compatible_with_code_field():
    msg = StatusMsg(status="ok", code="rpc.start.starting")
    assert msg.status == "ok"
    assert msg.code == "rpc.start.starting"
