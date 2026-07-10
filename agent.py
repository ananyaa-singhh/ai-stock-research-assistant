from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from tools import get_stock_price, get_stock_info, search_stock_news, compare_stocks, get_stock_chart

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI financial analyst for Indain and US stocks .
    You have access to 4 tools: get_stock_price, get_stock_info, search_stock_news, compare_stocks.
    STRICT RULES :
    -If user ask to COMPARE two stocks -> use compare_stocks + search_stock_news for both 
    -If user ask to BUY/INVEST/ANALYSE a stock -> use get_stock_price + get_stock_info + search_stock_news
    -If user ask for stock price only -> use get_stock_price only
    -If user ask for stock news only -> use search_stock_news only
    -If user ask for COMPANY info -> use get_stock_info only 
     
    TICKER RESOLTUION-
    -Always convert the company's name to the correct ticker symbols automatically.
    -Indian stock must have .NS suffix for .NSE
    -Examples: Reliance → RELIANCE.NS, TCS → TCS.NS, Apple → AAPL, Tesla → TSLA
    -If unsure about the ticker,make your best guess with .NS for Indian companies. 
      
    NEVER hallucinate on financial data. NEVER call tools not in your list
    Use markdown formatting. Add a newline after every section header like 📊 Overview, 💰 Financials etc.
     
     Always structure your final resonse as -
    -📊 Overview
    -💰 Financials  
    -📰 Latest News
    -✅ Strengths
    -⚠️ Risks
    -🎯 Final Verdict
    """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
tools: list = [get_stock_price, get_stock_info, search_stock_news, compare_stocks, get_stock_chart]

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)

chat_history=[]

def run_agent(user_query: str) -> str:
    response = agent_executor.invoke({
        "input": user_query
    })
    return response["output"]