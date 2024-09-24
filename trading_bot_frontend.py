import os
import streamlit as st
from openai import OpenAI

from trading_bot_backend import TradingBot

st.set_page_config(page_title='Trading Bot')
st.title("Trading Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()

user_query = st.chat_input('Ask a question')

if user_query:

    code = st.session_state.bot.code_generator(user_query=user_query)
    st.code(code)

    result = st.session_state.bot.code_executor(code)
    st.dataframe(result)