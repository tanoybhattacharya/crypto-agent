"""
scheduler.py — Runs agent.py every day at the configured time (DAILY_RUN_TIME in .env)
Start this once and leave it running (e.g., in the background or as a startup task).
"""
import schedule
import time
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import get_config
from agent import run as run_agent

# Logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "scheduler.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("scheduler")


def job():
    logger.info(f"⏰ Scheduled trigger fired at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_agent()


def main():
    config = get_config()
    run_time = config.get("DAILY_RUN_TIME", "09:00")

    logger.info("=" * 60)
    logger.info(f"📅 Crypto AI Scheduler started")
    logger.info(f"   Daily run time : {run_time} (local time)")
    logger.info(f"   Coins tracked  : {', '.join(config['COINS'])}")
    logger.info(f"   Report sent to : {config['RECIPIENT_EMAIL']}")
    logger.info("   Waiting for scheduled time... (Ctrl+C to stop)")
    logger.info("=" * 60)

    schedule.every().day.at(run_time).do(job)

    # Run immediately on first start so you can verify everything works
    logger.info("▶️  Running immediately on startup for verification...")
    run_agent()
    logger.info(f"✅ Startup run complete. Next run scheduled at {run_time} daily.")

    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user.")
