import requests
from client_utils.base_client import URL

TWEET_ID = 45
url = URL + f"/tweets/{TWEET_ID}"

response = requests.get(url)

if response.status_code == 200:
    print("Tweet Deleted!")
    print(response.json()["content"])
else:
    print(response.content)
