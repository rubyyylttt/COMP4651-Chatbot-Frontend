import json
import random
import requests
import streamlit as st
import textract

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from pathlib import Path

from openai import AzureOpenAI
from io import StringIO

"st.session_state object:", st.session_state      # for testing

apis = {
    "CHAT": "https://httpbin.org/get",# "https://v1/chat",
    "TRANSLATE": "https://httpbin.org/get",# "https://v1/translate",
    "DRAW":  "https://httpbin.org/get",# "https://v1/media",
    "MUSIC": "https://httpbin.org/get",#  "https://v1/music",
}

# ------ USER AUTHENTICATION ----- #
# Import the YAML dummy file
file_path = Path(__file__).parent / "user_credentials.yaml"
session_file_path = Path(__file__).parent / "sessions.yaml"

with file_path.open("rb") as file:
    config = yaml.load(file, Loader=SafeLoader)

with session_file_path.open("rb") as file:
    sessions = yaml.load(file, Loader=SafeLoader)

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

    if 'display' not in st.session_state:
        st.session_state['display'] = 'HOME' # or 'CHATROOM'

    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'CHAT'

    # ------ function for  ------ #
    def openSession(s_id):
        st.session_state['display'] = 'CHATROOM'
        st.session_state['s_id'] = s_id

    with st.sidebar:
        # buttons
        authenticator.logout()  

        # generate session buttons
        st.title("Chatrooms")

        newchat = st.button('➕ Create new chat', use_container_width=100)

        if newchat:
            st.session_state['display'] = 'HOME'
        
        for session_id, session_data in sessions['sessions'].items():
            title = 'Default'
            if session_data['mode'] == 'CHAT':
                title = '💬 ' + session_data['title']
            if session_data['mode'] == 'TRANSLATE':
                title = '🗣️ ' + session_data['title']
            if session_data['mode'] == 'DRAW':
                title = '🎨 ' + session_data['title']
            if session_data['mode'] == 'MUSIC':
                title = '🎵 ' + session_data['title']

            st.button(title, use_container_width=100, on_click=openSession, args=(session_id,))

        openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"


    model_name = "gpt-35-turbo"
    if st.session_state['display'] == 'HOME':
        st.subheader("Welcome, "+st.session_state["name"])
        
        st.caption("Start a new chat below")

        Chat, Translate, Draw, Music = st.tabs(["💬 Chat", "🗣️ Translate", "🎨 Draw", "🎵 Music"])

        with Chat:
            model_name = "gpt-35-turbo"

        with Translate:
            model_name = "gpt-35-turbo"
            # --------- upload document -------------
            uploaded_file = st.file_uploader(
                label="📄 upload document", 
                type=['doc', 'docx', 'pdf'],
                accept_multiple_files=False
            )

            if uploaded_file is not None:
                # To read file as bytes:
                # bytes_data = textract.process(uploaded_file)
                bytes_data = uploaded_file.getvalue()
                st.write(bytes_data)

                # To convert to a string based IO:
                # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                # st.write(stringio)

                # To read file as string:
                string_data = bytes_data.read()
                # string_data = stringio.read()
                st.write(string_data)


        with Draw:
            model_name = "gpt-35-turbo"
            # --------- upload media -------------
            uploaded_files = st.file_uploader(
                label=":frame_with_picture: upload image(s)", 
                type=['png', 'jpg'],
                accept_multiple_files=True
            )

            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    st.write("filename:", uploaded_file.name)
                    st.write(bytes_data)

        with Music:
            model_name = "gpt-35-turbo"
            # --------- upload media -------------
            uploaded_files = st.file_uploader(
                label="🎶 upload mp3", 
                type=['mp3', 'mp4'],
                accept_multiple_files=True
            )
            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    st.write("filename:", uploaded_file.name)
                    st.write(bytes_data)

    # when a user click a session button in the sidebar or create a new chatroom in the homepage
    elif st.session_state['display'] == 'CHATROOM':
        s_title = 'Default'
        session_items= sessions['sessions']
        sid = st.session_state['s_id'] 

        if session_items[sid]['mode'] == 'CHAT':
            s_title = '💬 ' + session_items[sid]['title']
        if session_items[sid]['mode'] == 'TRANSLATE':
            s_title = '🗣️ ' + session_items[sid]['title']
        if session_items[sid]['mode'] == 'DRAW':
            s_title = '🎨 ' + session_items[sid]['title']
        if session_items[sid]['mode'] == 'MUSIC':
            s_title = '🎵 ' + session_items[sid]['title']

        if session_items[sid]['messages'] is not None:
            st.session_state["messages"] =  session_items[sid]['messages']
        else:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        # interface
        st.title(s_title)
            
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
        # if "messages" not in st.session_state:
        #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        # for msg in st.session_state.messages:
        #     st.chat_message(msg["role"]).write(msg["content"])

        # if prompt := st.chat_input():
        #     if not openai_api_key:
        #         st.info("Please add your Azure OpenAI API key to continue.")
        #         st.stop()

        #     st.session_state.messages.append(
        #         {"role": "user", "content": prompt}
        #     )
        #     st.chat_message("user", avatar="🙋‍♂️").write(prompt)

        #     # setting up the OpenAI model
        #     client = AzureOpenAI(
        #         api_key=openai_api_key,
        #         api_version="2023-12-01-preview",
        #         azure_endpoint="https://hkust.azure-api.net/",
        #     )
        #     response = client.chat.completions.create(
        #         model=model_name,
        #         messages=st.session_state.messages
        #     )

        #     msg = response.choices[0].message.content
        #     st.session_state.messages.append({"role": "assistant", "content": msg})
        #     st.chat_message("assistant").write(msg)
            # --------- from original code end ---------