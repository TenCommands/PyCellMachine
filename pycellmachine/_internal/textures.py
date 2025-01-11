import pygame, sys, json

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


#print(splice(
#    r"texturepacks\default\assets\button.png",
#    r"texturepacks\default\data\button.json"
#))