# vibecoded project, i take no credit for it

import logging
import os
import sys

def get_log_path() -> str:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.config")
    folder = os.path.join(base, "dmfilter")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "blocked_log.txt")

LOG_PATH = get_log_path()

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def log_block(user, user_id, level, score, hits, message_preview):
    logging.info(
        f"BLOCKED | user={user} ({user_id}) | level={level} | "
        f"score={score} | cats={hits} | msg=\"{message_preview[:100]}\""
    )
