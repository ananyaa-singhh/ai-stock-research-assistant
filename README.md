# 📈 StockSense AI — Your AI Stock Research Assistant
An intelligent AI agent that provides real-time stock analysis, market insights, and investment research for both Indian (NSE/BSE) and US stocks.

🔗 **Live Demo:** [StockSense AI](https://ai-stock-research-assistant-asru7yuxgtezcyjbxu9zl6.streamlit.app/)

## 🚀 Features
- 💬 **Conversational AI** — Chat naturally, ask anything about stocks
- 📊 **Real-time Stock Data** — Live prices, PE ratio, market cap, 52W high/low
- 📰 **Latest News** — Web search for recent stock news
- 🔄 **Compare Stocks** — Side by side comparison with ROE, EPS, dividend yield
- 📈 **Price Charts** — Interactive 1-year price chart for any stock
- 🧠 **Multi-tool Reasoning** — Agent automatically picks the right tools
- 🎯 **Investment Analysis** — Structured reports with Strengths, Risks, Final Verdict
- 🏦 **Indian + US Markets** — NSE, BSE and all major US exchanges

## 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| Python | Core language |
| LangChain | AI Agent framework |
| Groq (LLaMA 3.3 70B) | LLM brain |
| yfinance | Real-time stock data |
| DuckDuckGo Search | Latest news |
| Plotly | Interactive charts |
| Streamlit | Web UI & deployment |

## 📁 Project Structure
stock-project/
├── app.py ← Streamlit chat UI
├── agent.py ← LangChain agent + Groq LLM
├── tools.py ← 6 stock research tools
├── requirements.txt
└── .env ← API keys (not pushed to GitHub)

## ⚙️ How It Works
User asks question
↓
LangChain Agent reads question
↓
Decides which tools to call automatically
↓
Fetches real-time data (Yahoo Finance + DuckDuckGo)
↓
Groq LLaMA 3.3 70B synthesizes the data
↓
Returns structured report with 6 sections

## 🔧 Setup & Installation

# Clone the repo
git clone https://github.com/ananyaa-singhh/ai-stock-research-assistant.git
cd ai-stock-research-assistant

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py

## 📊 Example Queries

- `"Should I invest in Reliance?"`
- `"Compare TCS and Infosys"`
- `"Latest news on HDFC Bank"`
- `"Tell me about Apple stock"`
- `"What is the current price of TATAGOLD.NS?"`
