# A program that stores a SQLite database of pulsar dynamic spectrum data.
# Takes user queries and behaves accordingly. [more desc here]
from __future__ import print_function
from __builtin__ import raw_input
import sys
import os
from pathlib2 import Path
import sqlite3
from astropy.io import fits
import numpy
import json
import datetime
import warnings
warnings.filterwarnings("ignore")

dataSize = 0  # the number of files in the database, initialize to 0
db_name = ""  # the global database name to work with

'''
Function to create a new empty database for storing fits files. Handles overwriting and naming errors.
'''


def makedb(db, replace):

    if db != "exit":

        conn = sqlite3.connect(db)
        c = conn.cursor()

        # try to create a new database in that name
        try:
            c.execute("""CREATE TABLE astrodata (
                name text,
                o text,
                mjd real,
                period real,
                dm real,
                bins integer,
                data BLOB,
                unique (name, o, mjd, period, dm, bins, data)
            )""")
            conn.commit()
            return db  # return new database name

        # catch an error if there is already a database with that name
        except sqlite3.Error as e:

            if replace == 1:  # if replace option is true

                print(
                    "A database named {0} already exists. Please enter another name for the database, or \'o\' to overwrite "
                    "the existing one. \n".format(db))
                inp = raw_input()  # get another database name
                print()

                # replace table if user wants to overwrite, but only if they are really sure
                if inp == "o":

                    print(
                        "ARE YOU SURE you want to overwrite your database? There's no going back. Type 'yes overwrite' to "
                        "proceed, or another name for your database.\n")
                    newinp = raw_input()  # record string for confirmation
                    print()

                    if newinp == "yes overwrite":
                        c.execute("DROP TABLE IF EXISTS astrodata")  # remove the existing database
                        conn = sqlite3.connect(db)  # use the original database name
                        c = conn.cursor()
                        c.execute("""CREATE TABLE astrodata (
                            name text,
                            o text,
                            mjd real,
                            period real,
                            dm real,
                            bins integer,
                            data BLOB,
                            unique (name, o, mjd, period, dm, bins, data)
                        )""")
                        conn.commit()
                        return db  # return database name
                    else:
                        makedb(newinp,1)  # make new database using the newest (third) input
                else:
                    makedb(inp,1)  # make new database using second input

            else:

                print("The database already exists, and you may not overwrite any existing information right now. " \
                      "Please enter another name.\n")

                inp = raw_input()  # get another database name
                print()

                return makedb(inp, 0)

        conn.close()


'''
Function to read files within a directory
'''


def readFile(directory):
    f = fits.open(directory)
    f.verify('fix')
    header = f[0].header  # header information stored in an array
    data = f[0].data  # binary data
    f.close()

    header = [str(header["SOURCE"]), str(header["ORIGIN"]), str(header["MJD"]), str(header["PERIOD"]),
              str(header["DM"]), str(header["NBINS"])]

    return header, data # header information and binary data


'''
Function to load fits files into an existing database. Currently working on inputting and extracting binary fits 
information.
'''


def load(directory):
    global dataSize, db_name
    log = open('log.txt', 'w+')  # file to log progress
    dirpath = Path(directory)

    #   Check if path is valid
    if dirpath.exists():
        stime = datetime.datetime.now()  # start time for operation
        print(".fits files will be loaded from " + directory + ".\n")
        filestoadd=[]  # list of all valid files to add to db

        # load files:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print("Finding files...\n")

        # if path is a directory, walk through it and find all fits files
        if dirpath.is_dir():
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith("dyn.fit") or file.endswith("dyn.fits"):
                        filestoadd.append(os.path.join(root, file))

        # otherwise, it is a file
        elif directory.endswith("dyn.fit") or directory.endswith("dyn.fits"):
            filestoadd.append(directory)

        else:
            print("No valid files found.")

        print("{0} files found.".format(len(filestoadd)))
        log.write("{0} files found.\n".format(len(filestoadd)))  # port to log.txt

        success = 0  # counter for successful adds

        for i in range(0, len(filestoadd)):
            print("Loading {0} out of {1} files: {2}".format(i + 1, len(filestoadd), filestoadd[i]))
            log.write("Loading {0} out of {1} files: {2}\n".format(i + 1, len(filestoadd), filestoadd[i]))  # port to log.txt

            try:
                header, data = readFile(filestoadd[i])
                # insert all header information as numerics and binary data as json object
                command = "INSERT INTO astrodata VALUES('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , ?)".format(
                    header[0], header[1], header[2], header[3], header[4], header[5])
                c.execute(command, (json.dumps(data.tolist()),))
                success += 1
            except Exception as e:
                print("Error loading file {0}: {1}".format(filestoadd[i], e.message))
                log.write("Error loading file {0}: {1}\n".format(filestoadd[i], e.message))  # port to log.txt

            conn.commit()
            dataSize += 1
            i += 1

        print("\nDone. {0} out of {1} files added successfully. See log.txt for more information.\n"
              .format(success, len(filestoadd)))
        log.write("\nDone. {0} out of {1} files added successfully.\n".format(success, len(filestoadd)))  # port to log.txt
        tottime = datetime.datetime.now() - stime  # elapsed time of operation
        print("Total time elapsed for adding: {0}\n".format(tottime))
        log.write("Total time elapsed for adding: {0}\n".format(tottime))  # port to log.txt
        conn.close()

    elif directory != "exit":
        print("Invalid directory. Type 'exit' to exit to the main menu or try again with a new input.\n")
        directory = raw_input()

        if directory != "exit":
            load(directory)

    log.close()


'''
Helper function to perform filtering and print out formatted values using a SQLite connection given a command.
'''


def filtprint(command):

    # first row of table
    print(" Pulsar Name |    Origin    |     MJD     |   Period   |    DM    | Bins ")
    print("-------------------------------------------------------------------------")

    stime = datetime.datetime.now()  # start time of operation
    global db_name
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(command)
    for i in c.fetchall():
        try:
            print(" %-12s| %-13s| %-12.4f| %-11.4f| %-9.4f| %-6d" % (i[0], i[1], i[2], i[3], i[4], i[5]))
            conn.commit()
        except Exception as e:
            print("Error fetching information.")
    tottime = datetime.datetime.now() - stime  # elapsed time of operation
    print("\nTotal time elapsed for process: {0}\n".format(tottime))


'''
Function to add filtered data into a subdatabase.
'''


def filtadd(command):

    # for global database
    global db_name
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    print("Would you like to put the filtered data into a new database? (y to confirm)\n")
    r = raw_input()
    print()

    if r == "y":
        print("Please enter a name for your new database.\n")
        # new input for database name
        inp = raw_input()
        print()

        newdb = makedb(inp,0)  # make the new database, save newest database name in case it changed during make()

        # for new database
        stime = datetime.datetime.now()  # start time of operation
        newconn = sqlite3.connect(newdb)
        newc = newconn.cursor()

        # loop through all the files in filter selection
        c.execute(command)
        results = c.fetchall()  # array of results
        for i in range(0, len(results)):

            print("Loading {0} out of {1} files...".format(i + 1, len(results)))
            j = results[i]

            # add into new database
            addcommand = "INSERT INTO astrodata VALUES('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , ?)".format(
                j[0], j[1], j[2], j[3], j[4], j[5])

            newc.execute(addcommand, (json.dumps(j[6]),))
            newconn.commit()
            conn.commit()

        newconn.close()
        conn.close()
        print("Filtered data added into database '{0}'.\n".format(newdb))
        tottime = datetime.datetime.now() - stime  # elapsed time of operation
        print("Total time elapsed for adding: {0}\n".format(tottime))



'''
Function to perform advanced filtering, with the user providing parameters in SQLite syntax.
'''


def advfilter():

    try:
        print("Please enter your filter query in advanced mode: \nSELECT * FROM database\n")
        r = raw_input()
        print()

        if r != "exit":
            command = "SELECT * FROM astrodata " + r
            filtprint(command)
            filtadd(command)
            advfilter()  # keep filtering

    except sqlite3.Error as e:
        print("Filter mode not recognized, try again or type 'exit' to return to main menu.")
        advfilter()


def sfilter():  # currently coded to only support one filter at a time
    global db_name

    print("Specify parameters to filter data. Each filter's parameters are inclusive of bounds, and should be " \
          "separated by 'and' or 'or'.")
    print("To exclude certain parameters, type 'not' before it.")
    print("Show all entries: 'all'")
    print("Pulsar name: 'name',(name)")
    print("Originating observatory: 'o',(name of origin)")
    print("MJD: 'mjd',(lower bound),(upper bound)")
    print("Period: 'p',(lower bound),(upper bound)")
    print("Dispersion measure: 'dm',(lower bound),(upper bound)")
    print("Number of bins: 'bins',(lower bound),(upper bound)")
    print()

    r = raw_input()
    print()

    command = ""  # sqlite command to run
    # command is in form: "param,low,high and param,value or not param,low,high" (an example)
    # the code would split the command by spaces
    # so each item would either be a comma separated filter or an operator keyword

    if r != "exit":

        if r == "all":
            command = "SELECT * FROM astrodata"
        else:
            command = "SELECT * FROM astrodata WHERE "

            flist = r.split(" ")  # split by spaces

            for q in flist:  # for each word in the query
                queries = q.split(",")  # get list of individual parameters of search if applicable

                if queries[0] == "and":
                    command = command + "AND"

                elif queries[0] == "or":
                    command = command + "OR"

                elif queries[0] == "name":
                    command = command + "(name=\'{0}\')".format(queries[1])

                elif queries[0] == "o":
                    command = command + "(o=\'{0}\')".format(queries[1])

                elif queries[0] == "mjd":
                    command = command + "(mjd BETWEEN {0} AND {1})".format(queries[1], queries[2])

                elif queries[0] == "p":
                    command = command + "(period BETWEEN {0} AND {1})".format(queries[1], queries[2])

                elif queries[0] == "dm":
                    command = command + "(dm BETWEEN {0} AND {1})".format(queries[1], queries[2])

                elif queries[0] == "bins":
                    command = command + "(bins BETWEEN {0} AND {1})".format(queries[1], queries[2])

                command = command + " "

        # try to filter with the command, output error if command is incorrect
        try:
            filtprint(command)
            filtadd(command)
            sfilter()  # keep filtering

        except sqlite3.Error as e:
            print("\nFilter mode not recognized, try again or type 'exit' to return to main menu.\n")
            sfilter()

def sort():

    print("Please specify the sorting parameter:")
    print("Pulsar name: 'name'")
    print("Originating observatory: 'o'")
    print("MJD: 'mjd'")
    print("Period: 'p'")
    print("Dispersion measure: 'dm'")
    print("Number of bins: 'bins'")
    print("Multiple parameters are allowed.")



'''
Function to connect to existing databases.
'''


def connect():
    global db_name

    # try to connect to database
    try:
        conn = sqlite3.connect(db_name) # connect to existing database file
        c = conn.cursor()

        # set dataSize to number of elements in it
        command = "SELECT Count(*) FROM astrodata"
        c.execute(command)
        global dataSize
        dataSize = c.fetchone()[0]

    # catch error if database doesn't exist
    except sqlite3.Error as e:

        if db_name == "exit":
            sys.exit()

        print(
            "There is no such database with the name {0}. Please enter a valid database name, or \'exit\' "
            "to quit.\n".format(db_name))
        db_name = raw_input()
        connect()

    # return name of connected database
    return db_name



'''
Main method to handle user input and queries.
'''


def main():
    global db_name
    print("Welcome to the pulsar database program!")

    # loop querying until user has made a valid decision
    while True:
        print("To create a new database, enter 'new'. To connect to an existing one, enter 'con'.")
        print("At any point, enter 'exit' to exit the program.\n")
        inp = raw_input()
        print()

        if inp == "new":
            print("What do you want to call the database?\n")
            db_name = raw_input()
            print()
            makedb(db_name,1)
            print()
            break
        elif inp == "con":
            print("Which database do you want to connect to?\n")
            db_name = raw_input()
            tmp = connect()
            db_name = tmp
            print()
            break
        elif inp == "exit":
            print("Exiting program.\n")
            sys.exit()
        else:
            print("Invalid command, please try again.\n")

    # loop querying forever
    while True:
        print("Your database '{0}' currently contains {1} files.".format(db_name, str(dataSize)))
        print("What would you like to do?")
        print("(load) - Load new data into the database")
        print("(sf) - Filter data using simple filtering mode.")
        print("(af) - Filter data using advanced filtering mode "
              "(recommended for those with SQLite syntax knowledge.) ")
        print("(sort) - Sort data by attribute.")
        print("(exit) - Exit the program\n")

        # take in user's input
        inp = raw_input()
        print()

        # cases
        if inp == "load":
            print("Specify directory containing .fits files to be imported.\n")
            directory = raw_input()
            print()
            load(directory)

        elif inp == "sf":
            sfilter()
            print()

        elif inp == "af":
            advfilter()
            print()

        elif inp == "sort":
            sort()
            print()

        elif inp == "exit":
            sys.exit()

        else:
            print("Command not valid. Please try again.\n")


# for main method on command line
if __name__ == "__main__": main()
