import requests
from client_utils.base_client import URL, token, token_type

TWEET_ID = 45
url = URL + f"/tweets/update/{TWEET_ID}"

HEADERS = {"Authorization": f"{token_type} {token}"}
TWEET = {"content": "Making a test... again"}

response = requests.put(url, json=TWEET, headers=HEADERS)

if response.status_code == 200:
    print("Tweet Updated!")
    print(response.json()["content"])
else:
    print(response.content)