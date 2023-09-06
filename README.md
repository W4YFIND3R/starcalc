# starcalc
A Starfield Mouse X Y Scale Calculator written in Python using 

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
- Uses Monoid text by https://larsenwork.com/monoid/

![image](https://github.com/W4YFIND3R/starcalc/assets/144207244/d36f9f42-d193-4484-8612-311215ad1594)

## Dependencies
- **Python**: This project requires Python version 3.x. [Download Python](https://www.python.org/downloads/)
- **Qt**: This project uses the Qt framework for its GUI components. Ensure you have the appropriate version of Qt installed.

