![](/git_assets/project_logo.png)
---
[![GNU License](https://img.shields.io/badge/License-GNU-blue.svg)](https://choosealicense.com/licenses/agpl-3.0/)
![GitHub commit activity](https://img.shields.io/github/last-commit/tencommands/PyCellMachine)

![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/tencommands/PyCellMachine/total?style=social)
![GitHub Repo stars](https://img.shields.io/github/stars/tencommands/PyCellMachine)


**Note**: There is currently still no functional gameplay.

## License

PyCellMachine is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3 (AGPL-3.0). This means:

- You can freely use, modify, and distribute this software
- If you modify and share this software, you must:
  - Make your modifications available under the same license
  - Share the source code when you deploy the software over a network
  - Preserve the original copyright notices
- Perfect for community collaboration while ensuring the project stays open source

The license text can be found in the [LICENSE](/LICENSE.md) file


## Some History

Cell Machine was originally created by Sam Hogan in 2019 as a simple cellular automata puzzle game where players place cells with different behaviors to solve levels. The game gained popularity through Sam's YouTube channel and inspired several fan-made mods and recreations:

- Cell Machine Mystic Mod (CMMM) - A popular mod adding new cells and features
- Cell Machine Indev - A recreation with enhanced capabilities
- CellLua - A Lua-based recreation with a ton of custom cells

The core gameplay revolves around cells that can:
- Move in different directions
- Generate new cells
- Destroy other cells 
- Rotate neighboring cells
- And more depending on the version

The simple yet engaging mechanics have created an active community that continues to design custom levels and expand upon the original concept.


## What Makes This Version Special?
This project is a complete recreation of the original Cell Machine game, but with a few key differences:

- ![](/git_assets/unity.png) This game was not built with Unity, like the other versions, but rather built from scratch meaning all interactions needed to be manual coded.
- ![](/git_assets/python.png) Python-based implementation for easy modification and expansion
- ![](/git_assets/github.png) Open-source codebase for transparency and collaboration right here on Github
- Modding API - The game is designed to be easily moddable with a custom modding API built with Python. [Learn more about the API here](/docs/modding_api.md)
- Coooperative Multiplayer - Players can work together to solve or create levels

### [To-Do List](/docs/todo.md)