"""
ai_analyzer.py — Uses Google Gemini to analyze news and generate BUY/HOLD/SELL recommendations
"""
import google.generativeai as genai
import logging
import re
import requests
import json

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


def analyze_gemini(prompt: str, api_key: str) -> str:
    """Run analysis using Google Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")
    logger.info("Sending news to Gemini for analysis...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"⚠️ Gemini analysis failed: {str(e)}"


def analyze_ollama(prompt: str, model: str, base_url: str) -> str:
    """Run analysis using local Ollama."""
    logger.info(f"Sending news to Ollama ({model}) for analysis...")
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "⚠️ No response from Ollama.")
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return f"⚠️ Ollama analysis failed: {str(e)}"


def analyze(news_data: dict[str, list[dict]], config: dict) -> str:
    """
    Analyze news for all coins and return a formatted recommendation string.
    Supports both Gemini and Ollama backends.
    """
    news_block = build_news_block(news_data)
    prompt = PROMPT_TEMPLATE.format(news_block=news_block)
    
    backend = config.get("AI_BACKEND", "gemini")

    if backend == "ollama":
        return analyze_ollama(
            prompt, 
            str(config.get("OLLAMA_MODEL", "llama3.2")), 
            str(config.get("OLLAMA_BASE_URL", "http://localhost:11434"))
        )
    else:
        api_key = config.get("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key is missing. Please check your .env file."
        return analyze_gemini(prompt, str(api_key))


if __name__ == "__main__":
    import json
    from config import get_config
    from news_fetcher import fetch_news
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    config = get_config()
    print(f"Fetching news for: {', '.join(config['COINS'])}")
    news = fetch_news(config["COINS"], config["NEWS_API_KEY"])

    print(f"Analyzing with {config['AI_BACKEND'].upper()} AI...")
    recommendation = analyze(news, config)

    print("\n" + "="*60)
    print("  🤖 AI RECOMMENDATION")
    print("="*60)
    print(recommendation)
