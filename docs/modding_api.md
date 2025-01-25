# ![](/git_assets/api_logo.png)
# Setup & Usage
## Prerequisites
- You must have PyCellMachine installed on your device.
- You must have a basic understanding of Python programming with knowledge on Classes, Functions, and Variables.
## Development environment setup
- It is recommended to use a code editor like Visual Studio Code or PyCharm when making your mod.
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [PyCharm](https://www.jetbrains.com/pycharm/)
## Required dependencies
- [Python](https://www.python.org/)
- [Pygame Community Edition](https://github.com/pygame-community/pygame-ce)

## File organization
![Namespace Folder](/git_assets/folder.png) `namespace`

![](/git_assets/I-.png) ![Cells Folder](/git_assets/folder.png) `cells`

![](/git_assets/I.png) ![](/git_assets/-.png) ![Cell Folder](/git_assets/folder.png) `cell_name`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Cell Image File](/git_assets/png.png)`cell.png`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Cell Python File](/git_assets/py.png)`cell.py`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/I-.png) ![Cell Json File](/git_assets/json.png)`cell.json`

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![Cell Json File](/git_assets/folder.png)`examples`* optional

![](/git_assets/I.png) ![](/git_assets/blank.png) ![](/git_assets/blank.png) ![](/git_assets/-.png) ![Cell Json File](/git_assets/json.png)`example.json`

![](/git_assets/I-.png) ![Mod Image File](/git_assets/png.png)`mod.png`

![](/git_assets/-.png) ![Mod Json File](/git_assets/json.png)`mod.json`

##

![Mod Json File](/git_assets/json.png)`mod.json`
```json
{
    "format": 1,
    "name": "Mod Name",
    "description": "Mod Description",
    "author": "Author(s)",
    "version": "1.0.0",
    "thumbnail_type": "png"
}
```
`format` - The format of the mod.json file.

`name` - The name of the mod.

`description` - A brief description of the mod.

`author` - The author(s) of the mod.

`version` - The version of the mod.

`thumbnail_type` - The type of thumbnail image to use.

##

![Cell Image File](/git_assets/png.png)`cell.png`

- Will be stretched to fit the cell meaning you can whatever size you want but it may only look good with 2<sup>^x</sup> size.
- On top of that [texturepacks](/docs/texturepacks.md) can override the texture. [See here](/docs/texturepacks.md#modded).

##

![Cell Json File](/git_assets/json.png)`cell.json`
```json
{
    "name": "Cell Name",
    "description": "Cell Description",
    "texture": {
        "mode": "standard",
        "texture": "texture.png"
    }
}
```
`name` - The name of the cell.

`description` - A brief description of the cell.

`texture` - The texture of the cell. (Subject to be moved to `cell.py` for more customization options)

- `mode` - The mode of the texture.

   - `standard` - Single image file that rotates when the cell rotates.
      - `texture` - The image file to use.
   - `animated` - Gif file that rotates when the cell rotates.
      - `texture` - The gif file to use.
   - `static` - Seperate image file for each cell rotation.
      - `0` - North
      - `1` - East
      - `2` - South
      - `3` - West
   - `static_animated` - Seperate gif file for each cell rotation.
      - `0` - North
      - `1` - East
      - `2` - South
      - `3` - West

##

![](/git_assets/folder.png)`examples/`* optional

Every ![](/git_assets/json.png)`.json` file in this folder will be loaded as an example of the cell and you can have as many as you wish.
```json
{
   "name": "Example Name",
   "description": "Example Description",
   "example": {
      "level": "code",
      "ticks": 10,
      "interactive": true
   }
}
```

`name` - The name of the example.

`description` - A brief description of the example.

`example` - The example.
   - `level` - The level save code of the example.
   - `ticks` - The amount of ticks to run the example for.
   - `interactive` - Allows for players to drag cells around or click on cells in the example.

##