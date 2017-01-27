import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'build_exe': {
        'packages': ['os'],
        'excludes': ['tkinter'],
        'include_files': ['data', 'images', 'sounds']
    }
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="pixelmek",
      version="0.2",
      description="PixelMek: The Game",
      options=build_options,
      executables=[Executable("pixelmek.py", base=base)])
