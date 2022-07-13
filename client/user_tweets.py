import requests
from client_utils.base_client import URL, token, token_type

url = URL + "/users/tweets"
HEADERS = {"Authorization": f"{token_type} {token}"}

response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    print("User's Tweets:")
    for tweet in response.json():
        print(f"id: {tweet['id']} - {tweet['content']}")
else:
    print(response.content)
