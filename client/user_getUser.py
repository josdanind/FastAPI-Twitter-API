import requests
from client_utils.base_client import URL

nickname = "hanshis"
url = URL + f"/users/user/{nickname}"

response = requests.get(url)

if response.status_code == 200:
    response = response.json()
    print(f"The user exists: {response['nickname']}")
else:
    print(response.content)