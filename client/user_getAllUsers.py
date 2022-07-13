import requests
from client_utils.base_client import URL

page = 0
limit = 10
url = URL + f"/users?page={page}&limit={limit}"

response = requests.get(url)

if response.status_code == 200:
    for user in response.json():
        print(user["nickname"])
else:
    print(response.content)
