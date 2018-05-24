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

## Technical Details
The main() method of the program directs user input and program output at the main startup menu. Functions in charge of each option listed in the "Capabilities and Usage Instructions" are called in the main() function, and handle subsequent user queries within themselves. Each time the program is run, one database file is selected to be operated on (ie. a SQLite connection will be opened to it), whether it be a new database or an existing one. Global variables include the total number of items and the name of the database. Within the code, user queries are checked for validity then translated to SQLite commands (represented by strings) that are executed by the connection to the database.

The SQLite table that is created upon the creation of a new database have columns that correspond the pulsar attributes represented by the dynamic spectra information, and each attribute is stored in SQLite in a corresponding data type: pulsar name (referred to as "name", has type text); the originating observatory name ("o", has type text); the pulsar's period ("period", has type real); the pulsar's dispersion measure ("dm", has type real); the number of bins ("bins", has type integer); the binary header information of the file ("data", has type BLOB). When a file representing a pulsar's dynamic spectrum information is stored, the information in the file will be parsed according to each column of the table, and a new row in the table is added. This means that any file lacking information in any attribute will generate an error and will not be added; this is part of "Known Issues" item 2.

## Capabilities and Usage Instructions
### Executing the Program
The program should be run on the command line within the directory of the Python program file, like so:
```
python ScintarcDatabase.py
```

At each step of the process, the program displays clear and helpful information that guides the user to input commands corresponding to what they wish to do. If an invalid command is entered, the program will prompt again. If the word "exit" is input, the program will return to the previous step, or exit the program completely if at the initial menu. 

The first step is to choose a database file to operate on: the user may either create a new database file, or open an existing one.

### Creating a new Database
Entering the "new" command will result in a prompt for a valid name for the new database to be created. The user will be prompted again if another database file of the same name already exists in the current directory.

### Opening an Existing Database
Entering "con" will result in a prompt for a valid name of an existing database file in the current directory. The user will be prompted again if no database file with that name exists.

After selecting a database, there will be a menu of options for operations to perform.

### Loading Files into the Database
To add files into the database, enter a directory containing files ending in "dyn.fits" or "dyn.fit". The program will recursively search through all contents of the directory and subdirectories, and add all the valid files within. Files that contain the same internal information as a file already in the database (duplicate data) will not be added.

### Filtering Files by Attribute
The program supports two modes to filter the database's files by attributes of pulsars (pulsar name "p", originating observatory "o", MJD "mjd", period "p", dispersion measure "dm", number of bins "bins"): simple mode ("sf" command: accepts verbose filtering commands suited towards those not familiar with SQLite syntax), and advanced mode ("af": accepts queries made in SQLite syntax and pipes the command directly into the SQLite connection for execution, which allows for more flexibility). Filtered results are displayed in a formatted table.

In simple mode, entering "all" will display an unsorted list of all the entries in the database; the same can be done with advanced mode by entering a blank command.

### Sorting Files by Attribute
The menu currently has an option for sorting database entries, but it is not functional; see "Known Issues" item 1.

### Exporting Filtered Files
After conducting a successful filtering query using either simple or advanced filtering mode, an option will arise to export the filtered items into a new database. Enter "y" to do so, or any other input to deny the option and enter another filter query. If the option is selected, a new database will be created with a user-specified name, and the results returned by the filtering query will be added to it. After this is done, the user is redirected back to the filtering menu for the original database being operated on so that another filtering command may be entered.

## Known Issues
1. The advanced filtering mode is coded to accept any SQLite command, but currently only handles filtering by attribute. With debugging and adjustments, sorting and other commands should theoretically be functional.
2. There are many errors documented in "logerrors.txt", and we are unsure if they are caused by the .fits/.fit files being corrupt or not representative of dynamic specra at all, or if there is something wrong in the code. See "Future Development Directions" item 1.

## Future Development Directions
1. Dissect the errors catalogued in "logerrors.txt", and determine whether the files themselves or the program is to blame for each of the different error types.
