cd pycellmachine
python -m \python\Scripts\activate
pyinstaller --onefile __main__.py --add-data="settings.json:." --add-data="mods/:." --add-data="texturepacks/:." --add-data="_internal/:." --hidden-import win32api