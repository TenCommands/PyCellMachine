import pygame, sys, json
from . import settings

pygame.init()

def splice(texture, splice_json):
    image = texture
    with open(splice_json, 'r') as f:
        splice_data = json.load(f)['slices']
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
    return rf"pycellmachine/texturepacks/{settings.get('texturepack')}/assets/{texture_path}"

def data(data_path):
    return rf"pycellmachine/texturepacks/{settings.get('texturepack')}/data/{data_path}"
