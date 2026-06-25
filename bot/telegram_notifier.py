"""
Telegram хабарлама жіберу.
.env файлында TELEGRAM_BOT_TOKEN және TELEGRAM_CHAT_ID қажет.
"""

import urllib.error
import urllib.parse
import urllib.request

from config.settings import settings


def _is_configured() -> bool:
    return bool(settings.telegram_bot_token and settings.telegram_chat_id)


def send_message(text: str, level: str = "info") -> bool:
    if not _is_configured():
        print("[WARN] Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
        return False

    icons = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️",
    }
    icon = icons.get(level, "ℹ️")
    full_text = f"{icon} <b>Sales Pipeline</b>\n\n{text}"

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = urllib.parse.urlencode(
        {
            "chat_id": settings.telegram_chat_id,
            "text": full_text,
            "parse_mode": "HTML",
        }
    ).encode("utf-8")

    request = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status == 200
    except urllib.error.URLError as e:
        print(f"[ERROR] Telegram send failed: {e}")
        return False


def send_success(message: str) -> bool:
    return send_message(message, level="success")


def send_warning(message: str) -> bool:
    return send_message(message, level="warning")


def send_error(message: str) -> bool:
    return send_message(message, level="error")
