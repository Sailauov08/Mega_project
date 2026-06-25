"""
Telegram bot тест:
python bot/test_telegram.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bot.telegram_notifier import send_success


if __name__ == "__main__":
    ok = send_success("Test message from Mega_project pipeline bot.")
    if ok:
        print("[OK] Telegram message sent")
    else:
        print("[FAIL] Could not send message. Check .env settings.")
