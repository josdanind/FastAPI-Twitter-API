import requests
from client_utils.base_client import URL

page = 0
limit = 10

url = URL + f"/tweets?page={page}&limit={limit}"

response = requests.get(url)

if response.status_code == 200:
    for tweet in response.json():
        print(tweet["content"])
else:
    print(response.content)