# starcalc
A Starfield Mouse X Y Scale Calculator

Starfield's Mouse scaling is not 1:1 X to Y, which was not optimal and did not feel right to me.

This is an attempt at making a Calculator to find the perfect values for setting up in StarfieldCustom.ini

StarfieldCustom.ini must exist in in "%USERPROFILE%\\Documents\My Games\Starfield\" on Windows, if it does not, create it. 

Features: 

- Calculates fMouseHeadingYScale= based on  fMouseHeadingXScale='s value * (resolution). Example: 0.021 * (2560/1440)
- Button that copies the calculated output to clipboard for you
- Button to open the Starfield config folder
- Has a colorful banner and icon
- Uses Monoid text by https://larsenwork.com/monoid/
