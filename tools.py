import yfinance as yf
from langchain.tools import tool
from duckduckgo_search import DDGS
import plotly.graph_objects as go

 
# ─────────────────────────────────────────
# TOOL 1: Get Live Stock Price
# ─────────────────────────────────────────
@tool
def get_stock_price(ticker: str) -> str:
    """
    Fetches the current/latest stock price and basic trading info.
    Use this when the user asks about the current price of a stock.
    For Indian stocks use NSE suffix e.g. 'TATAGOLD.NS', 'RELIANCE.NS'
    For US stocks just use ticker e.g. 'AAPL', 'TSLA'
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
 
        if data.empty:
            return f"Could not fetch data for {ticker}. Please check the ticker symbol."
 
        latest = data.iloc[-1]
        price  = round(latest["Close"], 2)
        high   = round(latest["High"], 2)
        low    = round(latest["Low"], 2)
        volume = int(latest["Volume"])
 
        return (
            f"Stock: {ticker}\n"
            f"Current Price: {price}\n"
            f"Today's High:  {high}\n"
            f"Today's Low:   {low}\n"
            f"Volume:        {volume:,}"
        )
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"
 
 
# ─────────────────────────────────────────
# TOOL 2: Get Stock Info / Fundamentals
# ─────────────────────────────────────────
@tool
def get_stock_info(ticker: str) -> str:
    """
    Fetches company details and fundamental data like PE ratio, market cap,
    sector, 52-week high/low etc.
    Use this when the user wants to understand the company behind the stock.
    For Indian stocks use NSE suffix e.g. 'RELIANCE.NS', 'TCS.NS'
    For US stocks just use ticker e.g. 'GOOGL', 'MSFT'
    """
    try:
        stock = yf.Ticker(ticker)
        info  = stock.info
 
        name        = info.get("longName", ticker)             #to fetch from dictionary
        sector      = info.get("sector", "N/A")
        industry    = info.get("industry", "N/A")
        market_cap  = info.get("marketCap", "N/A")
        pe_ratio    = info.get("trailingPE", "N/A")
        week_high   = info.get("fiftyTwoWeekHigh", "N/A")
        week_low    = info.get("fiftyTwoWeekLow", "N/A")
        summary     = info.get("longBusinessSummary", "No description available.")[:300]
 
        # Format market cap nicely
        if isinstance(market_cap, (int, float)):                   #is market_cap really a number
            if market_cap >= 1_000_000_000:                        # Python's way of making big numbers readable
                market_cap = f"{market_cap / 1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                market_cap = f"{market_cap / 1_000_000:.2f}M"
 
        return (
            f"Company:      {name}\n"
            f"Sector:       {sector}\n"
            f"Industry:     {industry}\n"
            f"Market Cap:   {market_cap}\n"
            f"PE Ratio:     {pe_ratio}\n"                          # price to earning ratio = stock price * earning per share  
            f"52W High:     {week_high}\n"
            f"52W Low:      {week_low}\n"
            f"About:        {summary}..."
        )
    except Exception as e:
        return f"Error fetching info for {ticker}: {str(e)}"
 
 
# ─────────────────────────────────────────
# TOOL 3: Search Latest Stock News
# ─────────────────────────────────────────
@tool
def search_stock_news(query: str) -> str:
    """
    Searches the internet for the latest news about a stock or company.
    Use this when the user wants recent news, updates, or market sentiment.
    Pass the company name or stock ticker as the query.
    Example: 'Tata Gold ETF news' or 'Apple stock news 2024'
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query + " stock news", max_results=5))
 
        if not results:
            return "No news found for this query."
 
        news_summary = f"Latest news for '{query}':\n\n"
        for i, result in enumerate(results, 1):                             # for loop to get # i=1,i-2...
            title = result.get("title", "No title")
            body  = result.get("body", "")[:200]
            link  = result.get("href", "")
            news_summary += f"{i}. {title}\n   {body}...\n   Source: {link}\n\n"
 
        return news_summary
    except Exception as e:
        return f"Error searching news: {str(e)}"
 
# ─────────────────────────────────────────
# TOOL 4: Compare Two Stocks
# ─────────────────────────────────────────
@tool
def compare_stocks(tickers: str) -> str:
    """
    Compares two stocks side by side — price, PE ratio, 52W high/low, market cap.
    Pass two ticker symbols separated by a comma.
    Example: 'AAPL,MSFT' or 'RELIANCE.NS,TCS.NS'
    """
    try:
        ticker_list = [t.strip() for t in tickers.split(",")]
        if len(ticker_list) != 2:
            return "Please provide exactly 2 ticker symbols separated by a comma. E.g. 'AAPL,MSFT'"
 
        results = []
        for ticker in ticker_list:
            stock = yf.Ticker(ticker)
            info  = stock.info
            data  = stock.history(period="1d")
 
            price = round(data.iloc[-1]["Close"], 2) if not data.empty else "N/A"
 
            results.append({
                "ticker":     ticker,
                "name":       info.get("longName", ticker),
                "price":      price,
                "pe":         info.get("trailingPE", "N/A"),
                "week_high":  info.get("fiftyTwoWeekHigh", "N/A"),
                "week_low":   info.get("fiftyTwoWeekLow", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "dividend_yield":info.get("dividendYield","N/A"),
                "roe":         info.get("returnOnEquity","N/A"),
                "eps":         info.get("trailingEps","N/A"),
                "recommendation":info.get("recommendationKey","N/A")
            })
 
        a, b = results[0], results[1]
 
        return str(results)
    except Exception as e:
        return f"Error comparing stocks: {str(e)}"
     

# ─────────────────────────────────────────
# TOOL 5: Get Stock Chart
# ─────────────────────────────────────────
@tool
def get_stock_chart(ticker: str) -> str:
    """
    Fetches historical price data for charting.
    Returns 1 year of daily closing prices.
    For Indian stocks use .NS suffix e.g. 'TCS.NS'
    For US stocks just use ticker e.g. 'AAPL'
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")

        if data.empty:
            return f"No chart data found for {ticker}"

        dates  = data.index.strftime("%Y-%m-%d").tolist()
        prices = round(data["Close"], 2).tolist()

        return str({"dates": dates, "prices": prices, "ticker": ticker})
    except Exception as e:
        return f"Error fetching chart data: {str(e)}"

@tool        
def get_stock_fundamentals(ticker: str) -> str:
    """
    Fetches detailed fundamental data for a stock, including last dividend, 
    ,earnings dates, analyst recommendations/upgrades/downgrades,.
    For Inidan stocks use .NS suffix eg. 'TCS.NS'
    For US stocks just use ticker eg.'AAPL'
    """
    try:
        stock=yf.Ticker(ticker)
        info=stock.info
        dividends=stock.dividends    #shares of company's profit paid to shareholders
        earnings_dates=stock.earnings_dates #quarterly earnings report dates
        recommendations=stock.recommendations #analyst recommendations

        last_dividend=dividends.iloc[-1] if not dividends.empty else "N/A"
        
        return str({
            "ticker": ticker,
            "last_dividend": str(last_dividend),    #str beacuse LLM can read it easily 
            "earnings_dates":str(earnings_dates.head(3)) if earnings_dates is not None else "N/A",
            "recommendations": str(recommendations.head(3)) if recommendations is not None else "N/A"
        })
    except Exception as e :
        return f"Error fetching fundamanetals for {ticker}:{str(e)}"