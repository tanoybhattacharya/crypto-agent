# 📊 Crypto AI Daily Agent

A Python agent that **automatically fetches crypto news, analyzes it with Google Gemini AI, and emails you a daily BUY/HOLD/SELL recommendation** — for any coins you configure.

---

## ✨ Features

- 📄 **Configurable coins** — edit `coins.txt` to track any cryptocurrency
- 🤖 **AI-powered analysis** — Google Gemini reads the news and generates recommendations
- 📧 **Beautiful HTML email** — color-coded BUY/HOLD/SELL badges per coin
- ⏰ **Daily scheduler** — runs automatically at your configured time
- 📝 **Daily logs** — all runs saved in `logs/`

---

## 🗂️ Project Structure

```
crypto-agent/
├── coins.txt          ← Add/remove coins here (one per line)
├── .env               ← Your API keys (copy from .env.example)
├── .env.example       ← Template for .env
├── config.py          ← Loads settings
├── news_fetcher.py    ← Fetches news via NewsAPI
├── ai_analyzer.py     ← Generates recommendations via Gemini
├── email_sender.py    ← Sends HTML email via Gmail
├── agent.py           ← One-shot run (all steps)
├── scheduler.py       ← Daily scheduler (run once, leave running)
├── requirements.txt
└── logs/              ← Auto-created on first run
```

---

## 🚀 Setup Guide

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Get your API keys

#### NewsAPI (Free)
1. Go to [https://newsapi.org](https://newsapi.org) → **Get API Key**
2. Register a free account
3. Copy your API key

#### Google Gemini API (Free)
1. Go to [https://aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** → **Create API key**
3. Copy your API key

#### Gmail App Password (Free — uses your existing Gmail)
1. Make sure your Gmail has **2-Step Verification enabled**
   - Google Account → Security → 2-Step Verification
2. Go to: **Google Account → Security → App Passwords**
3. Select app: `Mail`, device: `Windows Computer`
4. Click **Generate** → copy the 16-character password

> ⚠️ Use the **App Password**, NOT your normal Gmail password.

---

### Step 3 — Configure your `.env` file

```bash
copy .env.example .env
```

Then edit `.env` with your values:

```ini
NEWS_API_KEY=abc123yourkeyhere
GEMINI_API_KEY=AIza...yourkeyhere

SMTP_EMAIL=yourgmail@gmail.com
SMTP_APP_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=anyemail@example.com

DAILY_RUN_TIME=09:00
```

---

### Step 4 — Configure your coins

Edit `coins.txt` — one coin name per line:

```
XRP
Ethereum
Bitcoin
Solana
Cardano
```

> 💡 Use the common name (e.g., `Ethereum`, not `ETH`). The agent uses these as news search keywords.

---

## ▶️ Running the Agent

### One-shot run (test it now):
```bash
python agent.py
```

### Daily scheduler (run once, keep it running):
```bash
python scheduler.py
```

The scheduler will:
1. **Run immediately** on startup so you can verify it works
2. **Run every day** at the time set in `DAILY_RUN_TIME`

---

## 🔍 Testing Individual Components

```bash
# Test configuration loading
python config.py

# Test news fetching
python news_fetcher.py

# Test AI analysis
python ai_analyzer.py

# Test email sending (sends a sample email)
python email_sender.py
```

---

## 📬 Sample Email Output

Each email includes:
- 🟢 **BUY** / 🟡 **HOLD** / 🔴 **SELL** badge per coin
- Key signals extracted from news
- Confidence level and risk rating
- Actionable recommendation for today

---

## 🪟 Auto-start on Windows (Optional)

To run the scheduler automatically on Windows startup:

1. Press `Win + R` → type `shell:startup` → Enter
2. Create a shortcut to:
   ```
   pythonw.exe C:\Users\admin\.gemini\antigravity\scratch\crypto-agent\scheduler.py
   ```
3. The agent will run silently in the background every day

---

## ⚠️ Disclaimer

This tool is for **informational purposes only**. The AI-generated recommendations are not financial advice. Always do your own research before making investment decisions.
