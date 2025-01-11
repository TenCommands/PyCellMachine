import os, json, settings

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

def info(mod):
    # get mod.json from mod folder
    with open(f"mods/{mod}/mod.json") as f:
        return json.load(f)

def format(type, input):
    if type == "version":
        version_nums = input.split(".")
        for i in range(len(version_nums)):
            version_nums[i] = int(version_nums[i]) * 10 ** (2 - i)
        return sum(version_nums)


class Mod():
    def __init__(self, format, name, description, author, version, github_url, thumbnail_type):
        self.format = format
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.github_url = github_url
        self.thumbnail_type = thumbnail_type

    def _update(self):
        print(format("version", self.version))
        # get  latest version from update_url
        

mods = []
for mod in os.listdir("mods"):
    if mod in enabled:
        mod_info = info(mod)
        mods.append(Mod(
            format=mod_info['format'],
            name=mod_info['name'], 
            description=mod_info['description'],
            author=mod_info['author'],
            version=mod_info['version'],
            github_url=mod_info['update_url'],
            thumbnail_type=mod_info['thumbnail_type']
        ))