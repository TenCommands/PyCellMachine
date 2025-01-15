import json

def get(path=None):
    try:
        with open("pycellmachine/settings.json", 'r') as f:
            if path is None:
                return json.load(f)
            else:
                return json.load(f)[path]
    except FileNotFoundError:
        print("settings.json not found")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in settings.json")
        return None


def save(data):
    with open("pycellmachine/settings.json", 'w') as f:
        json.dump(data, f, indent=4)