# To-Do List
## Bugs 🐞
- Texturepacks Screen not indicating actively selected pack.
- Make [build.bat](/build.bat) build an executable file which can be run from anywhere to play the game without needing to activate the executable from terminal.
## Modding API ![](/git_assets/python.png)
```
Everything Between Here Is Required For Gameplay To Exist
```
- Cell Class
   - Holds initial information that defines the functionality of a Cell
- Tile Class
   - Holds current Cell information such as position, rotation, etc.
- Grid Class
   - Holds all of the Tiles
- Menu Class
   - Allows for modders to create Menus which can contain all Menu objects and Grids which users can interact with.
   - Able to get information about the Menu to enact actions on the Cell such as positions of Cells within a Grid in that Menu being used to determine the overall functionality of the Cell.
- Examples
   - A folder within the Cell defining folder allowing for the mod creator to create examples of how the Cell works.
- Mod Loading

```
```

- Dev Tools
- Debug Console

## Audio
- Music from CMMM+MM
- Music specifically made for PyCellMachine
- UI sound effects
- Cell Sound Effects
- Note Cell
   - Will play a specified audio file when a cell collides with it and then output said Cell on the opposite side when it's done playing.
