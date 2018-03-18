# Scintarc-Database
A SQLite database application for storing, filtering, and creating sub-databases of fits data (dynamic spectra), written in Python. Files are uploaded from local directories, and portable database files containing the selected fits files are created. Users can enter queries to filter data flexibly based on a wide range of parameters, and create smaller databases containing the search results. Users may also connect to existing databases if the database files are present. This program provides a portable way to transfer and maintain libraries of pulsar data, as well as a friendly interface to sort through an otherwise disorganized collection for relevant information for certain projects.

This program was developed by Shana Li and Jude Fernandes, but this branch and version of the program is maintained by Shana Li, and differs from the master and Jude's version by structure and functionality.

## Package Contents
* ScintarcDatabase.py - The original master version of the program, right before it was branched off.
* ScintarcDatabase_shana.py - Shana's version of the program.
* README.md - This file.

## Capabilities
* Adding local fits files to new databases, including headers and binary data.
* Connecting to local database files and performing actions on them.
* Filter dynamic spectra by pulsar name, origin, MJD, period, DM, and bins.
* Simple filtering option for basic and, or operations.
* Advanced filtering option for custom SQLite-syntax based queries.
* Save filter results into a new database and export the database file.
* Process indicators and timestamps for filtering and file adding.

## Differences to Master Version
* Uses the json library to add binary data into the database.
* Able to connect to existing databases.
* Advanced and simple filtering modes both working.
* Able to create databases out of filtered results.
* Many structural changes in the code, which improve the function, readability, and interface of the program.

### Prerequisites

The Astropy distribution of Python, version 2.7 or above, is required to run this program.

### Running the Program
To run the program on the command line:

```
python ScintarcDatabase_shana.py
```

Then, follow the on-screen instructions to create a new database or connect to an existing one (which requires providing the directory and name of the db file to connect to). 
Type "exit" at any point in the program to go to a previous step or exit the program at the main menu.

## Authors

* **Shana Li** - https://github.com/shanalii (branch developer)
* **Jude Fernandes** - https://github.com/juderoque (master branch partner)
