import json
import requests
from client_utils.base_client import URL

url = URL + "/users/login"

LOGIN = {
    "username": "string",
    "password": "stringst"
}

session = requests.Session()
response = session.post(url, LOGIN)
response = json.loads(response.content.decode('utf-8'))

with open("./token.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(response))