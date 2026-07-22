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
    ("system", """You are an expert AI financial analyst assistant for Indian and US stocks.

        You have access to these tools: get_stock_price, get_stock_info, search_stock_news, compare_stocks, get_stock_chart, get_stock_fundamentals.

        CONVERSATION RULES:
        - For greetings like "hi", "hello" → respond naturally in 1-2 lines, ask what stock they need help with. NO tools needed.
        - For general questions → answer conversationally, NO structured format.

        STRICT RULES:
        - If user asks to COMPARE two stocks → use compare_stocks + search_stock_news for both
        - If user asks to BUY/INVEST/ANALYSE/SHOULD I → use get_stock_price + get_stock_info + search_stock_news → show ALL 6 sections including Final Verdict
        - If user asks for NEWS only → use search_stock_news only
        - If user asks for PRICE only → use get_stock_price only
        - If user asks for COMPANY INFO only → use get_stock_info only. Show Overview and Financials ONLY, NO Final Verdict.

        TICKER RESOLUTION:
        - Always convert company names to correct ticker symbols automatically.
        - Indian stocks must have .NS suffix for NSE.
        - Examples: Reliance → RELIANCE.NS, TCS → TCS.NS, Apple → AAPL, Tesla → TSLA

        MEMORY:
        - Always refer to previous messages in the conversation.
        - If user says "which one is better" after a comparison, remember what was compared.
      
        FORMATTING RULES:
        - Always use these exact section headers with emojis:
        📊 **Overview**
        💰 **Financials**
        📰 **Latest News**
        ✅ **Strengths**
        ⚠️ **Risks**
        🎯 **Final Verdict**
        - Always add a blank line between each section.
        - Never skip emojis in headers.
        NEVER hallucinate financial data. NEVER call tools not in your list.
        """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
tools: list = [get_stock_price, get_stock_info, search_stock_news, compare_stocks, get_stock_chart]

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)

def run_agent(user_query: str, chat_history: list = []) -> str:
    history_text = ""
    try:
        if chat_history and len(chat_history) > 0:
            recent = chat_history[-4:]
            for msg in recent:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"
    except:
        history_text = ""

    full_input = f"Previous conversation:\n{history_text}\nCurrent question: {user_query}" if history_text else user_query
    
    response = agent_executor.invoke({
        "input": full_input,
    })
    return response["output"]