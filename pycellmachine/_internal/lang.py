import pygame, sys, os, json
from . import settings
from . import get_resource_path
from . import load_data

# function to load language data from the lang.json file found in the active texturepack
def load_lang(text, texturepack=settings.get('texturepack'), lang=settings.get('options')['other']['language'][0]):
    # Try loading from chosen texturepack first
    try:
        if texturepack != 'default':
            custom_lang = load_data(get_resource_path(rf".\texturepacks\{texturepack}\text\lang.json"))
            if text in custom_lang[lang]:
                return custom_lang[lang][text]
    except (KeyError, FileNotFoundError):
        pass
    # Fall back to default texturepack
    return load_data(get_resource_path(rf"_internal\assets\default\text\lang.json"))[lang][text]
