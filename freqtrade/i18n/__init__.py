import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from freqtrade.constants import Config
from freqtrade.persistence.key_value_store import KeyValueStore


SUPPORTED_LANGUAGES = {"en", "vi"}
DEFAULT_LANGUAGE = "en"
USER_LANGUAGE_KEY = "user_language_preferences"
TELEGRAM_LANGUAGE_KEY = "telegram_language"


def normalize_language(language: str | None) -> str:
    if not language:
        return DEFAULT_LANGUAGE
    lang = language.lower().strip()
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


@lru_cache(maxsize=8)
def _load_catalog(language: str) -> dict[str, str]:
    catalog_path = Path(__file__).parent / "catalogs" / f"{language}.json"
    if not catalog_path.exists():
        return {}
    with catalog_path.open("r", encoding="utf-8") as fp:
        loaded = json.load(fp)
    return loaded if isinstance(loaded, dict) else {}


def translate(key: str, language: str | None = None, **params: Any) -> str:
    lang = normalize_language(language)
    message = _load_catalog(lang).get(key) or _load_catalog(DEFAULT_LANGUAGE).get(key) or key
    if params:
        try:
            return message.format(**params)
        except KeyError:
            return message
    return message


def get_default_language(config: Config) -> str:
    telegram_lang = config.get("telegram", {}).get("language")
    if telegram_lang:
        return normalize_language(telegram_lang)
    return normalize_language(config.get("api_server", {}).get("default_language"))


def _load_user_language_map() -> dict[str, str]:
    raw = KeyValueStore.get_string_value(USER_LANGUAGE_KEY)
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {str(k): normalize_language(str(v)) for k, v in parsed.items()}
    except json.JSONDecodeError:
        return {}
    return {}


def get_user_language(username: str, config: Config) -> str:
    languages = _load_user_language_map()
    return normalize_language(languages.get(username, get_default_language(config)))


def set_user_language(username: str, language: str) -> str:
    normalized = normalize_language(language)
    languages = _load_user_language_map()
    languages[username] = normalized
    KeyValueStore.store_value(USER_LANGUAGE_KEY, json.dumps(languages))
    return normalized

