from decouple import config
import json

HOST = config('HOST')
PORT = config('PORT',default=8000, cast=int)

URL = f"http://{HOST}:{PORT}/api/v1"
TOKEN_PATH = "./token.json"

with open(TOKEN_PATH, "r", encoding="utf-8") as file:
    jwt = json.loads(file.read())

token = jwt["access_token"]
token_type = jwt["token_type"]

