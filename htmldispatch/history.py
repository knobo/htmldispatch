import json
from datetime import datetime

from .config import HISTORY_FILE, ensure_config_dir

MAX_HISTORY = 500


def load_history():
    ensure_config_dir()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def save_history(history):
    ensure_config_dir()
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY:], f, indent=2)


def add_entry(url, browser, profile, rule_name=None):
    history = load_history()
    history.append({
        "url": url,
        "browser": browser,
        "profile": profile,
        "rule": rule_name,
        "timestamp": datetime.now().isoformat(),
    })
    save_history(history)
