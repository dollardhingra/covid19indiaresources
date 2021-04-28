import os
import logging

LOGFILE = os.environ.get("LOGFILE", "mylogs.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Telegram Constants
# Default to a fake Telegram token for testing purposes if none is provided.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", f"{'1' * 10}:{'A' * 35}")
# Current message character limit is 4096
# https://core.telegram.org/method/messages.sendMessage
# https://limits.tginfo.me/en
TELEGRAM_MESSAGE_CHAR_LIMIT = 4096
