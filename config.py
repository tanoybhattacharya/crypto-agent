"""
config.py — Loads environment variables and reads coins.txt
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def get_coins() -> list[str]:
    """Read coins.txt and return a list of coin names (non-empty lines, stripped)."""
    coins_file = BASE_DIR / "coins.txt"
    if not coins_file.exists():
        raise FileNotFoundError(f"coins.txt not found at {coins_file}. Please create it.")
    coins = [
        line.strip()
        for line in coins_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not coins:
        raise ValueError("coins.txt is empty. Please add at least one coin name.")
    return coins


def get_config() -> dict:
    """Return all configuration values. Raises if required keys are missing."""
    required = {
        "NEWS_API_KEY": os.getenv("NEWS_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "SMTP_EMAIL": os.getenv("SMTP_EMAIL"),
        "SMTP_APP_PASSWORD": os.getenv("SMTP_APP_PASSWORD"),
        "RECIPIENT_EMAIL": os.getenv("RECIPIENT_EMAIL"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please copy .env.example to .env and fill in your values."
        )
    return {
        **required,
        "DAILY_RUN_TIME": os.getenv("DAILY_RUN_TIME", "09:00"),
        "COINS": get_coins(),
    }


if __name__ == "__main__":
    config = get_config()
    print("✅ Configuration loaded successfully.")
    print(f"   Coins to track : {', '.join(config['COINS'])}")
    print(f"   Daily run time : {config['DAILY_RUN_TIME']}")
    print(f"   Recipient email: {config['RECIPIENT_EMAIL']}")
