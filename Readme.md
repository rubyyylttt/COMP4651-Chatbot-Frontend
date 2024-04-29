# Build Chatbot: COMP4461

To run, following the following steps:

1. create a new python environment (search online if you don't know)
2. `pip install -r requirements.txt`
3. `pip3 install streamlit-authenticator` [for user authentication service]
4. `streamlit run cloud_chatbot.py` [modified for cloud chatbot project]

  
- `streamlit run domain_chatbot.py` [reference code from HCI lab code]

## User Authentication
Reference: https://github.com/mkhorasani/Streamlit-Authenticator/tree/main?tab=readme-ov-file#authenticatelogin

user_credentials.yaml: a dummy file for user db.

hash_pwd.py: helper for hashing the pwds stored in the yaml file.

Right now there's two acc:

username: jsmith

password: abc

username: rbriggs

password: def


## TODO

1. Create acc button on user auth page
  
2. Create new chat interface, that's where all 4 buttons is displayed
  <img width="468" alt="Screenshot 2024-04-29 at 11 06 04 AM" src="https://github.com/edithsyl/COMP4651-Chatbot-Frontend/assets/69338737/4a306bfe-b17f-4a0c-87d1-e39c14524dc7">

3. Sessions on sidebar
  <img width="285" alt="Screenshot 2024-04-29 at 11 06 34 AM" src="https://github.com/edithsyl/COMP4651-Chatbot-Frontend/assets/69338737/1128a447-78f9-4ccf-a88a-1751992a10a7">


