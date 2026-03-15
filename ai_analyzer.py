"""
ai_analyzer.py — Uses Google Gemini to analyze news and generate BUY/HOLD/SELL recommendations
"""
import google.generativeai as genai
import logging
import re

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are a professional cryptocurrency market analyst. You have been given the latest news headlines and summaries for multiple cryptocurrencies.

Analyze the news sentiment and market signals for each coin, then provide a clear daily recommendation.

---
{news_block}
---

For EACH coin listed above, provide your analysis in EXACTLY this format:

## [COIN NAME]
**Recommendation:** BUY | HOLD | SELL
**Confidence:** High | Medium | Low
**Sentiment:** Bullish | Neutral | Bearish

**Key Signals:**
- Signal 1 from the news
- Signal 2 from the news
- Signal 3 (if available)

**Action for Today:**
Write 2-3 sentences explaining what action the investor should consider today and why, based on the news.

**Risk Level:** Low | Medium | High
**Timeframe:** Short-term (1-7 days)

---

Be concise, data-driven, and base your analysis strictly on the provided news.
Include a brief disclaimer at the very end: "⚠️ This is AI-generated analysis for informational purposes only. Not financial advice."
"""


def build_news_block(news_data: dict[str, list[dict]]) -> str:
    """Format the news data into a readable block for the prompt."""
    blocks = []
    for coin, articles in news_data.items():
        lines = [f"### {coin} News:"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. **{a['title']}** ({a['source']})")
            desc = a.get("description", "")
            if desc and desc != "No description available.":
                lines.append(f"   {desc[:200]}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def analyze(news_data: dict[str, list[dict]], gemini_api_key: str) -> str:
    """
    Analyze news for all coins and return a formatted recommendation string.
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    news_block = build_news_block(news_data)
    prompt = PROMPT_TEMPLATE.format(news_block=news_block)

    logger.info("Sending news to Gemini for analysis...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"⚠️ AI analysis failed: {str(e)}\nPlease check your GEMINI_API_KEY."


if __name__ == "__main__":
    import json
    from config import get_config
    from news_fetcher import fetch_news
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    config = get_config()
    print(f"Fetching news for: {', '.join(config['COINS'])}")
    news = fetch_news(config["COINS"], config["NEWS_API_KEY"])

    print("Analyzing with Gemini AI...")
    recommendation = analyze(news, config["GEMINI_API_KEY"])

    print("\n" + "="*60)
    print("  🤖 AI RECOMMENDATION")
    print("="*60)
    print(recommendation)
