"""
agent.py — Main orchestrator: fetch news → AI analysis → send email
Run this directly for a one-shot execution of the full pipeline.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import get_config
from news_fetcher import fetch_news
from ai_analyzer import analyze
from email_sender import send_email

# ── Logging setup ─────────────────────────────────────────────────────────────
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"agent_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8"),
    ],
)
logger = logging.getLogger("agent")


def run():
    """Execute the full daily crypto recommendation pipeline."""
    start = datetime.now()
    logger.info("=" * 60)
    logger.info(f"🚀 Crypto AI Agent — Starting run at {start.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # 1. Load configuration
    try:
        config = get_config()
        logger.info(f"✅ Config loaded | Coins: {', '.join(config['COINS'])} | Recipient: {config['RECIPIENT_EMAIL']}")
    except (FileNotFoundError, EnvironmentError) as e:
        logger.error(f"❌ Configuration error: {e}")
        return False

    # 2. Fetch news
    logger.info("📰 Step 1/3 — Fetching latest news...")
    news_data = fetch_news(config["COINS"], config["NEWS_API_KEY"])
    for coin, articles in news_data.items():
        logger.info(f"   {coin}: {len(articles)} article(s) found")

    # 3. AI analysis
    logger.info("🤖 Step 2/3 — Generating AI recommendations via Gemini...")
    recommendation = analyze(news_data, config["GEMINI_API_KEY"])
    logger.info(f"   Recommendation length: {len(recommendation)} chars")

    # 4. Send email
    logger.info(f"📧 Step 3/3 — Sending email to {config['RECIPIENT_EMAIL']}...")
    success = send_email(
        smtp_email=config["SMTP_EMAIL"],
        smtp_password=config["SMTP_APP_PASSWORD"],
        recipient_email=config["RECIPIENT_EMAIL"],
        coins=config["COINS"],
        recommendation_text=recommendation,
    )

    elapsed = (datetime.now() - start).total_seconds()
    if success:
        logger.info(f"✅ Run completed successfully in {elapsed:.1f}s")
    else:
        logger.error(f"❌ Run finished with errors in {elapsed:.1f}s")

    return success


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
