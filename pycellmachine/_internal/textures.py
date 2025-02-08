import pygame, sys, os, json
from . import settings
from . import get_resource_path
from . import load_data

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

def asset(texture_path):
    # First try loading from selected texture pack
    if settings.get('texturepack') != 'default':
        custom_path = get_resource_path(rf".\texturepacks\{settings.get('texturepack')}\assets\{texture_path}")
        if os.path.exists(custom_path):
            return custom_path
    # Fall back to default if texture doesn't exist
    return get_resource_path(rf"_internal\assets\default\assets\{texture_path}")

def data(data_path):
    if settings.get('texturepack') != 'default':
        custom_path = get_resource_path(rf".\texturepacks\{settings.get('texturepack')}\data\{data_path}")
        if os.path.exists(custom_path):
            return load_data(custom_path)
    return load_data(get_resource_path(rf"_internal\assets\default\data\{data_path}"))

def texturepack(pack=settings.get('texturepack'), path="/"):
    if pack == 'default':
        return get_resource_path(rf"_internal\assets\default{path}")
    else:
        return get_resource_path(rf".\texturepacks\{pack}{path}")

def load_texture(path):
    return pygame.image.load(asset(path)).convert_alpha()