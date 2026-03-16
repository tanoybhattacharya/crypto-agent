# 📊 Crypto AI Daily Agent

A Python agent that **automatically fetches crypto news, analyzes it with AI, and emails you a daily BUY/HOLD/SELL recommendation** — for any coins you configure. Now supports both **Google Gemini** (Cloud) and **Ollama** (Local Llama 3.2).

---

## ✨ Features

- 📄 **Configurable coins** — edit `coins.txt` to track any cryptocurrency
- 🤖 **Hybrid AI-powered analysis** — Choose between Google Gemini (Cloud) or Ollama (Local Llama 3.2)
- 🎛️ **Interactive Selection** — Pick your model at startup via a simple terminal menu
- 📧 **Beautiful HTML email** — color-coded BUY/HOLD/SELL badges per coin
- ⏰ **Daily scheduler** — runs automatically at your configured time
- 📝 **Daily logs** — all runs saved in `logs/`

---

## 🗂️ Project Structure

```
crypto-agent/
├── coins.txt          ← Add/remove coins here (one per line)
├── .env               ← Your API keys & Backend choice
├── cli_utils.py       ← Helper for interactive selection
├── config.py          ← Loads settings
├── news_fetcher.py    ← Fetches news via NewsAPI
├── ai_analyzer.py     ← Generates recommendations (Gemini or Ollama)
├── email_sender.py    ← Sends HTML email via Gmail
├── agent.py           ← One-shot run with interactive prompt
├── scheduler.py       ← Daily scheduler (interactive choice at startup)
├── requirements.txt
└── logs/              ← Auto-created on first run
```

---

## 🚀 Setup Guide

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — (Optional) Install Ollama for Local AI

If you want to run analysis for free on your own hardware:
1. Download Ollama from [ollama.com](https://ollama.com)
2. Open terminal and run: `ollama pull llama3.2`
3. Keep the Ollama app running in the background.

### Step 3 — Get your API keys

#### NewsAPI (Required)
1. Go to [https://newsapi.org](https://newsapi.org) → **Get API Key**
2. Register a free account and copy your key.

#### Google Gemini API (Optional - for Cloud AI)
1. Go to [https://aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** and copy it.

#### Gmail App Password (Required for Email)
1. Enable **2-Step Verification** on your Google Account.
2. Go to **Google Account → Security → App Passwords**.
3. Generate a password for `Mail` on a `Windows Computer`.

---

### Step 4 — Configure your `.env` file

```bash
copy .env.example .env
```

Edit `.env` with your values:

```ini
# AI Backend: 'gemini' or 'ollama'
AI_BACKEND=ollama

# NewsAPI key
NEWS_API_KEY=your_key_here

# For Gemini (if used)
GEMINI_API_KEY=your_key_here

# For Ollama (if used)
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# Email Configuration
SMTP_EMAIL=yourgmail@gmail.com
SMTP_APP_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=anyemail@example.com

DAILY_RUN_TIME=09:00
```

---

### Step 5 — Configure your coins

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

When you start the agent or scheduler, you will be prompted to select your model:

### One-shot run:
```bash
python agent.py
```

### Daily scheduler:
```bash
python scheduler.py
```
*(You'll choose the backend once at startup; the scheduler will use that choice daily.)*

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
