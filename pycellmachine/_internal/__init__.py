import pygame, sys, os, json

def get_resource_path(relative_path):
    # Get absolute path to resource
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    
    return os.path.join(base_path, relative_path)

def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
