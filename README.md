# starcalc
A Starfield Mouse X Y Scale Calculator written in Python. Get the latest release from the [releases page](https://github.com/W4YFIND3R/starcalc/releases).

Starfield's Mouse scaling is not 1:1 X to Y, which was not optimal and did not feel right to me.

This is an attempt at making a Calculator to find the perfect values for setting up in StarfieldCustom.ini

StarfieldCustom.ini must exist in in "%USERPROFILE%\\Documents\My Games\Starfield\" on Windows, if it does not, create it. 

Features: 

- Calculates fMouseHeadingYScale= based on  fMouseHeadingXScale='s value * (resolution). Example: 0.021 * (2560/1440)
- Dropdown resolution selection with a user enterable field if a custom resolution not in the dropdown is required
- Button that copies the calculated output to clipboard for you
- Button to open the Starfield config folder
- User field to enter a manual fMouseHeadingXScale= if the default program's 0.021 isn't optimal
- Checkbox for including a line to disable mouse acceleration
- Has a colorful banner and icon
- Uses less than 1MB of System Memory
- Uses Monoid text by https://larsenwork.com/monoid/

![image](https://github.com/W4YFIND3R/starcalc/assets/144207244/d36f9f42-d193-4484-8612-311215ad1594)

## Items used to build the Windows release
- **Python** Version 3.11.5: [Download Python](https://www.python.org/downloads/)
- **PySide6** Version: 6.5.2: PySide6 is the official Python module from the Qt for Python project, which provides access to the complete Qt 6.0+ framework. https://pypi.org/project/PySide6/
- **PyInstaller** Version 5.13.2: PyInstaller bundles a Python application and all its dependencies into a single package. [PyPI Link](https://pypi.org/project/pyinstaller/)

Example build command using PyInstaller to pack everything into a single .exe for Windows: 

``` pyinstaller --onefile --noconsole --add-data="Monoid-Regular.ttf;." --add-data="starcalcsplash.png;." --add-data="starcalcicon.ico;." --icon="starcalcicon.ico" starfield_mouse_scale_calc.py ```
