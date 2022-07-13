import requests
from client_utils.base_client import URL, token, token_type

url = URL + "/users/delete"
HEADERS = {"Authorization": f"{token_type} {token}"}

response = requests.delete(url, headers=HEADERS)

if response.status_code == 200:
    response = response.json()
    print(f"The user was deleted: {response['nickname']}")
else:
    print(response.content)
