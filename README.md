# simplified-g-code-interpreter

## Description

The goal of the project is to simulate the execution of g-code, a widely used CNC programming language, with Python.

## Table of Contents

- [Logic of the interpreter](#logic-of-the-interpreter)
- [Validity](#validity)
- [MachineClient class](#machineclient-class)
- [Supported commands](#supported-commands)
- [To-do](#to-do)

## Logic of the interpreter

### Validity

The file is first read in its entirety to run preliminary checks on the validity of the code before simulating it being run. This somewhat mirrors the behavior of some of the devices that may run those kinds of tests themselves. Here, the following requirements are asked of the code:

- The library 'sys' can be loaded when not running the file as an imported module
- The file is read in its entirety
- Access to the file is granted
- The symbol '%' at the start and the end of the file
- Comments are allowed at the end of the line or on their own lines
- Skip everything in a line after the symbol '/'
- Have an acceptable program number
- Outside of comments, and the beginning and the end, only have numbers, certain letters, spaces, and decimal points
- Have spaces between commands (this will most likely be changed in the future)
- Commands have to be of certain length and only have one letter

### MachineClient class

Rapid movement has been taken to mean moving first along both of the axis (in the case of moving in two dimensions) equally and if one of the directions still has length to go after the other one has finished getting to the correct coordinate value, continue moving in this direction until the program reaches the correct coordinate. This is opposed to linear movement that is both influenced by the feed rate and goes as a straight line between the starting point and the end point. The program remembers which movement type is used and it does not need to be specified explicitly each time, unless it changes of course.

### Supported commands

- G0 OR G00 => Set movement to 'rapid'
- G1 OR G01 => Set movement to 'linear'
- G17 => Set plane to 'xy'
- G18 => Set plane to 'zx'
- G19 => Set plane to 'yz'
- G20 => Set units to inches (not fully implemented)
- G21 => Set units to millimeters
- G28 => Go to home position (assumed to be (0,0,0))
- M3 OR M03 => Turn spindle rotation on (does not implement rotation direction)
- M5 OR M05 => Turn spindle rotation off
- M9 OR M09 => Turn spindle coolant on
- M10 => Turn spindle coolant off
- Sxx => Set spindle rotation speed to xx
- Fxx => Set spindle feed rate to xx
- Txx => Change tool to xx
- Xxx => Move 'x' coordinate to xx position
- Yxx => Move 'y' coordinate to xx position
- Zxx => Move 'z' coordinate to xx position

## To-do

- [ ] Write more unit tests
- [ ] Fully implementing G20
- [ ] Implementing other 'G' and 'M' commands
- [ ] Allow having no spaces between commands
