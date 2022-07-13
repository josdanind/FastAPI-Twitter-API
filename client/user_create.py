import requests
from client_utils.base_client import URL

url = URL + "/users/signup"

user = {
    "email": "hanshis@example.com",
    "nickname": "hanshis",
    "first_name": "Hans",
    "last_name": "Loca",
    "birth_date": "2022-07-13",
    "password": "hanshis1234"
}

response = requests.post(url, json=user)

if response.status_code == 201:
    response = response.json()
    print(f"The user was crated: {response['nickname']}")
else:
    print(response.content)
