# helper file for hashing pwds in user_credentials.yaml

import yaml
from yaml.loader import SafeLoader

from pathlib import Path

from streamlit_authenticator.utilities.hasher import Hasher

# Import the YAML file
file_path = Path(__file__).parent / "user_credentials.yaml"

with file_path.open("rb") as file:
    data = yaml.load(file, Loader=SafeLoader)


# Iterate over the usernames and hash their passwords
for username, user_data in data['credentials']['usernames'].items():
    print(Hasher._hash(user_data['password']))
    user_data['password'] = Hasher._hash(user_data['password'])


with file_path.open("w") as file:
    yaml.dump(data, file, default_flow_style=False)