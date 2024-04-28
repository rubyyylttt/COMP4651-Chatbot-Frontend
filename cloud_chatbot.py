import json
import random
import requests
import streamlit as st
from openai import AzureOpenAI

"st.session_state object:", st.session_state
if 'mode' not in st.session_state:
    st.session_state['mode'] = 'CHAT'

def my_function(val):
    st.write("The value is:", val)
    st.write("The mode is:", mode)
    if isinstance(val,str):
        mode = val
    else:
        mode = 'ERROR'
    st.write("2The value is:", val)
    st.write("2The mode is:", mode)

with st.sidebar:
    st.button('Chat', on_click={my_function('CHAT')})
    st.button('Translate', on_click={my_function('TRANSLATE')})
    st.button('Draw', on_click={my_function('DRAW')})
    st.button('Music', on_click={my_function('MUSIC')})

    openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"

model_name = "gpt-35-turbo"

if mode == 'CHAT':
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

elif mode == 'TRANSLATE':
    st.title("💬 Translate")
elif mode == 'DRAW':
    st.title("💬 Draw")
elif mode == 'MUSIC':
    st.title("💬 Music")
elif mode == 'ERROR':
    print('error')