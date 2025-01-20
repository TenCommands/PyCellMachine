import json
import os
import sys

def get(path=None):
    # Get the directory containing the executable
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    settings_path = os.path.join(base_path, "settings.json")
    
    try:
        with open(settings_path, 'r') as f:
            if path is None:
                return json.load(f)
            else:
                return json.load(f)[path]
    except FileNotFoundError:
        print(f"settings.json not found at {settings_path}")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in settings.json")
        return None

def save(data):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    settings_path = os.path.join(base_path, "settings.json")
    with open(settings_path, 'w') as f:
        json.dump(data, f, indent=4)
