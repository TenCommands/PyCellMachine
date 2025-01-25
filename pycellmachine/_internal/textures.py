import pygame, sys, os, json
from . import settings

#pygame.init()

def splice(texture, splice_json):
    image = texture

    if type(splice_json) == str:
        splice_data = load_data(splice_json)
    else:
        splice_data = splice_json
    
    slices = {}
    for splice in splice_data:
        data = splice_data[splice]
        # Calculate width and height for subsurface
        width = data[1][0] - data[0][0] + 1
        height = data[1][1] - data[0][1] + 1
        slices[splice] = image.subsurface(
            (data[0][0],
             data[0][1],
             width,
             height))
    return slices

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

def asset(texture_path):
    return get_resource_path(rf".\texturepacks\{settings.get('texturepack')}\assets\{texture_path}")

def data(data_path):
    return load_data(get_resource_path(rf".\texturepacks\{settings.get('texturepack')}\data\{data_path}"))

def texturepack(pack=settings.get('texturepack'), path="/"):
    return get_resource_path(rf".\texturepacks\{pack}{path}")

def load_texture(path):
    return pygame.image.load(asset(path)).convert_alpha()

def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)