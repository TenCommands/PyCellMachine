import json

def get(path):
    with open("settings.json") as f:
        return json.load(f)[path]