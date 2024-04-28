import json
import random
import requests
import streamlit as st

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from pathlib import Path

from openai import AzureOpenAI

# "st.session_state object:", st.session_state      # for testing

apis = {
    "CHAT": "https://httpbin.org/get",# "https://v1/chat",
    "TRANSLATE": "https://httpbin.org/get",# "https://v1/translate",
    "DRAW":  "https://httpbin.org/get",# "https://v1/media",
    "MUSIC": "https://httpbin.org/get",#  "https://v1/music",
}

# ------ USER AUTHENTICATION ----- #
# Import the YAML file
file_path = Path(__file__).parent / "user_credentials.yaml"
with file_path.open("rb") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator object
authenticator = stauth.Authenticate(    
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# retrieve the name, authentication status, and username from Streamlit's session state using st.session_state["name"], st.session_state["authentication_status"], and st.session_state["username"]
authenticator.login()

if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")

if st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")

if st.session_state["authentication_status"]: # USER AUTHENTICATION is success

# ------ MAIN PAGE ----- #

    st.subheader("Welcome, "+st.session_state["name"])
    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'CHAT'

    with st.sidebar:
        # buttons
        authenticator.logout()  
        chat_bu = st.button('💬 Chat', use_container_width=100)
        translate_bu = st.button('🗣️ Translate', use_container_width=100)
        draw_bu = st.button('🎨 Draw', use_container_width=100)
        music_bu = st.button('🎵 Music', use_container_width=100)

        openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"

        # switch between different mode
        if chat_bu:
            st.session_state['mode'] = 'CHAT'
        if translate_bu:
            st.session_state['mode'] = 'TRANSLATE'
        if draw_bu:
            st.session_state['mode'] = 'DRAW'
        if music_bu:
            st.session_state['mode'] = 'MUSIC'

    model_name = "gpt-35-turbo"

    if st.session_state['mode'] == 'CHAT':
        st.title("💬 Chatbot")
        # --------- upload media -------------
        uploaded_files = st.file_uploader(
            label=":frame_with_picture: upload image", 
            type=['png', 'jpg'],
            accept_multiple_files=True
        )
        
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)
            st.write(bytes_data)
        
        # --------- sending requests ---------
        d = {
                'id': 'value1', 
                'userId': 'value2',
                'sessionId': 'CHAT',
                'input':{
                    'role': 'user',
                    'content': {
                        'type': 'text',
                        'url': 'url',
                        'prompt': 'prompt'
                    }
                }
            }
        test = {"firstName": "John", "lastName": "Smith"}
        r = requests.post(apis.get(st.session_state['mode']), data=test)
        st.caption("print r: "+r.text)
        # --------- sending requests ---------
        
        # --------- from original code ---------
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
            st.chat_message("user", avatar="🙋‍♂️").write(prompt)

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
            # --------- from original code end ---------
    elif st.session_state['mode'] == 'TRANSLATE':
        st.title("🗣️ Translate")
    elif st.session_state['mode'] == 'DRAW':
        st.title("🎨 Draw")
    elif st.session_state['mode'] == 'MUSIC':
        st.title("🎵 Music")
    else:
        st.title("ERROR")