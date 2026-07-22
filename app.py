import streamlit as st
from agent import run_agent
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(page_title="Nivesh Copilot", page_icon="📈", layout="centered")
st.title("📈 StockSense AI")
st.markdown("*Your AI Financial Research Assistant*")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about any stock...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            answer = run_agent(user_input, st.session_state.messages)
        st.markdown(answer)

        ticker = None
        for word in user_input.upper().split():
            if ".NS" in word or ".BO" in word:
                ticker = word
                break

        if not ticker:
            for word in answer.upper().split():
                if ".NS" in word or ".BO" in word:
                    ticker = word
                    break

                if word in ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"]:
                    ticker = word
                    break

        if ticker:
            st.session_state.last_ticker = ticker
        elif "last_ticker" in st.session_state:
            ticker = st.session_state.last_ticker

        if ticker:
            data = yf.Ticker(ticker).history(period="1y")
            if not data.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data["Close"],
                    mode="lines",
                    name=ticker,
                    line=dict(color="green", width=2)
                ))
                fig.update_layout(
                    title=f"{ticker} - 1 Year Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    template="plotly_dark"
                )
                st.plotly_chart(fig)

    st.session_state.messages.append({"role": "assistant", "content": answer})