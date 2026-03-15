"""
news_fetcher.py — Fetches top news articles for each coin using NewsAPI
"""
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def fetch_news(coins: list[str], api_key: str, articles_per_coin: int = 5) -> dict[str, list[dict]]:
    """
    Fetch the latest news articles for each coin.

    Returns:
        dict: { "CoinName": [ {"title": ..., "description": ..., "url": ..., "publishedAt": ...}, ... ] }
    """
    client = NewsApiClient(api_key=api_key)
    results = {}

    # Look back 24 hours
    from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")

    for coin in coins:
        try:
            logger.info(f"Fetching news for: {coin}")
            # Improved query to reduce noise
            query = f'"{coin}" AND (crypto OR cryptocurrency OR blockchain)'
            response = client.get_everything(
                q=query,
                from_param=from_date,
                language="en",
                sort_by="relevancy",
                page_size=articles_per_coin,
            )
            articles = response.get("articles", [])
            results[coin] = [
                {
                    "title": a.get("title", "No title"),
                    "description": a.get("description") or a.get("content") or "No description available.",
                    "url": a.get("url", ""),
                    "publishedAt": a.get("publishedAt", ""),
                    "source": a.get("source", {}).get("name", "Unknown"),
                }
                for a in articles
            ]
            if not results[coin]:
                logger.warning(f"No news articles found for {coin}. Using placeholder.")
                results[coin] = [{
                    "title": f"No recent news found for {coin}",
                    "description": "No articles were returned for this query in the past 24 hours.",
                    "url": "",
                    "publishedAt": "",
                    "source": "N/A",
                }]
        except Exception as e:
            logger.error(f"Error fetching news for {coin}: {e}")
            results[coin] = [{
                "title": f"Error fetching news for {coin}",
                "description": str(e),
                "url": "",
                "publishedAt": "",
                "source": "Error",
            }]

    return results


if __name__ == "__main__":
    import json
    from config import get_config
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    config = get_config()
    news = fetch_news(config["COINS"], config["NEWS_API_KEY"])

    for coin, articles in news.items():
        print(f"\n{'='*50}")
        print(f"  📰 {coin} — {len(articles)} articles")
        print(f"{'='*50}")
        for i, a in enumerate(articles, 1):
            print(f"  {i}. [{a['source']}] {a['title']}")
            print(f"     {a['description'][:120]}...")
