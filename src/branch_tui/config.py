import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".branch-tui-config"


def save_token(token: str):
    CONFIG_FILE.write_text(token.strip())
    os.chmod(CONFIG_FILE, 0o600)


def load_token() -> str:
    env_token = os.getenv("GITHUB_TOKEN")
    if env_token:
        return env_token

    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()

    return ""
