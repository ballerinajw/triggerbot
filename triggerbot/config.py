# vibecoded project, i take no credit for it

import json
import os
import sys

def get_config_path() -> str:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.config")
    folder = os.path.join(base, "dmfilter")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "config.json")

CONFIG_PATH = get_config_path()

def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"token": "", "level": 2}

def save_config(token: str, level: int):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"token": token, "level": level}, f)
