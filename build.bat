python -m PyInstaller --onefile --noconsole --hidden-import pygame --hidden-import pycellmachine._internal --collect-all pygame --add-data "D:\GitHub\PyCellMachine\pycellmachine\*;pycellmachine" --add-data "D:\GitHub\PyCellMachine\pycellmachine\_internal\*;pycellmachine\_internal" --add-data "D:\GitHub\PyCellMachine\pycellmachine\texturepacks\*;pycellmachine\texturepacks" --add-data "D:\GitHub\PyCellMachine\pycellmachine\mods\*;pycellmachine\mods" --icon=pycellmachine/_internal/assets/logo.png pycellmachine\__main__.py