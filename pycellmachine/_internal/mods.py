import os, json
from . import settings

enabled = settings.get()['mods']

###
{
    "format": 1,
    "name": "Conway's GoL",
    "description": "Conways Game of Life",
    "author": "TauCommands",
    "version": "1.0.0",
    "update_url": "https://github.com/tencommands/pycellmachine/mods/conway",
    "thumbnail_type": "gif"
}
###

def is_override(asset):
    # if the active texturepack has the same asset as the mod, return true
    if os.path.exists(rf"./texturepacks/{settings.get('texturepack')}/assets/{asset}"):
        return True
    return False

def path(mod, path):
    return rf"./mods/{mod}{path}"

def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
