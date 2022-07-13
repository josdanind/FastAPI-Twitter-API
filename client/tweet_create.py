import requests
from client_utils.base_client import URL, token, token_type

url = URL + f"/tweets/post"
HEADERS = {"Authorization": f"{token_type} {token}"}
TWEET = {"content": "Making a test."}

response = requests.post(url, json=TWEET,  headers=HEADERS)

if response.status_code == 201:
    print("Tweet created!")
    print(response.json()["content"])
else:
    print(response.content)