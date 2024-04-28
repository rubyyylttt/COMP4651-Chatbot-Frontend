import json
import random
import requests
import streamlit as st
from openai import AzureOpenAI

"st.session_state object:", st.session_state

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'CHAT'

with st.sidebar:
    chat_bu = st.button('Chat')
    translate_bu = st.button('Translate')
    draw_bu = st.button('Draw')
    music_bu = st.button('Music')

    if chat_bu:
        st.session_state['mode'] = 'CHAT'
    if translate_bu:
        st.session_state['mode'] = 'TRANSLATE'
    if draw_bu:
        st.session_state['mode'] = 'DRAW'
    if music_bu:
        st.session_state['mode'] = 'MUSIC'

    openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"

model_name = "gpt-35-turbo"

if st.session_state['mode'] == 'CHAT':
    st.title("💬 Chatbot")


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your Azure OpenAI API key to continue.")
            st.stop()

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        st.chat_message("user").write(prompt)

        # setting up the OpenAI model
        client = AzureOpenAI(
            api_key=openai_api_key,
            api_version="2023-12-01-preview",
            azure_endpoint="https://hkust.azure-api.net/",
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages
        )

        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

elif st.session_state['mode'] == 'TRANSLATE':
    st.title("💬 Translate")
elif st.session_state['mode'] == 'DRAW':
    st.title("💬 Draw")
elif st.session_state['mode'] == 'MUSIC':
    st.title("💬 Music")
else:
    st.title("ERROR")