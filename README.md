# Scintarc-Database
A SQLite database program written in Python that stores, filters, and exports pulsar dynamic spectra data files, developed by Shana Li and Jude Fernandes with professor Dan Stinebring. The program should be executed on the command line, and has a user-friendly interface with clear instructions for commands that the user can use to manipulate databases.

## Contents
* README.md: this file.
* ScintarcDatabase.py: the Python file for the program.
* log.txt: a log of the program's output when attempting to add all the files ending in "dyn.fits" in the master data drive (currently in the possession of Dan Stinebring). Includes all the successes, errors, and total runtime.
* logerrors.txt: a log of the errors encountered when attempting to add all the files ending in "dyn.fits" in the master data drive. Errors include: an attribute of pulsar data not found (possibly due to data corruption or the file not being dynamic spectrum information), file too large.

## System Requirements
* A command line program that can run Python (eg. Unix Terminal, Microsoft Command Prompt)
* Python 2.6 or higher (for Python 2, some changes to the code is required; instructions are included in the code itself)
* Anaconda 2 or higher

## Capabilities and Usage Instructions

### Executing the Program
The program should be run on the command line within the directory of the Python program file, like so:
```
python ScintarcDatabase.py
```

At each step of the process, the program displays clear and helpful information that guides the user to input commands corresponding to what they wish to do. If an invalid command is entered, the program will prompt again. If the word "exit" is input, the program will return to the previous step, or exit the program completely if at the initial menu. 

The first step is to choose a database file to operate on: the user may either create a new database file, or open an existing one.

### Creating a new Database

### Opening an Existing Database

### Loading Files into the Database

### Filtering Files by Attribute

### Exporting Filtered Files

## Known Issues

## Future Development Directions
