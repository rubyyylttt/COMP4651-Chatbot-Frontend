# Build Chatbot: COMP4461

To run, following the following steps:

1. create a new python environment (search online if you don't know)
2. `pip install -r requirements.txt`
3. `pip3 install streamlit-authenticator textract` [for user authentication service, upload file]
4. `streamlit run cloud_chatbot.py` [modified for cloud chatbot project]

  
domain_chatbot.py: reference code from HCI lab code

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

1. Upload component does not work 
2. User input box and user submission
3. show previous chats/messages on screen
4. Create account button on user auth page




