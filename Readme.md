# Build Chatbot: COMP4461

To run, following the following steps:

- create a new python environment (search online if you don't know)

- `pip install -r requirements.txt`
- `pip3 install streamlit-authenticator` [for user authentication service]

- `streamlit run cloud_chatbot.py` [modified for cloud project]
- `streamlit run domain_chatbot.py`[from HCI lab code]


## User Authentication
Reference: https://github.com/mkhorasani/Streamlit-Authenticator/tree/main?tab=readme-ov-file#authenticatelogin

user_credentials.yaml is a dummy file for user db.
hash_pwd.py is for hashing the pwds stored in the yaml file.

Right now there's two acc:
username: jsmith
password: abc

username: rbriggs
password: def