import requests
from client_utils.base_client import URL, token, token_type

TWEET_ID = 39 
url = URL + f"/tweets/delete/{TWEET_ID}"

HEADERS = {"Authorization": f"{token_type} {token}"}

response = requests.delete(url, headers=HEADERS)

if response.status_code == 200:
    print("Tweet Deleted!")
    print(response.json()["content"])
else:
    print(response.content)