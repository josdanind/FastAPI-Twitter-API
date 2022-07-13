from urllib import response
import requests
from client_utils.base_client import URL, token, token_type

url = URL + "/users/update"
HEADERS = {"Authorization": f"{token_type} {token}"}

user = {
    "nickname": "El Poder"
}

response = requests.put(url, json=user, headers=HEADERS )

if response.status_code == 200:
    response = response.json()
    print(f"User Updated: {response['nickname']}")
else:
    print(response.content)