import json

def get():
    with open("settings.json") as f:
        return json.load(f)