#A program that stores a SQLite database of pulsar dynamic spectrum data.
#Takes user queries and behaves accordingly. [more desc here]
from __builtin__ import raw_input
import sys
import os
from pathlib2 import Path
import sqlite3
from astropy.io import fits as pyfits

#fields
dataSize = 0 #the number of files in the database, initialize to 0



#main method
def main():

    print("Welcome to the pulsar database!")
    print("What do you want to call the database?")
    db_name = raw_input()
    make(db_name)
    print("Your database currently contains " + str(dataSize) + " files.")


    while(True): #loop querying forever

        print("What would you like to do?")
        print("(load) - Load new data into the database")
        print("(filter) - Filter data with specific parameters")
        print("(exit) - Exit the program")

        #take in user's input
        inp = raw_input()

        #cases
        if (inp == "load"):
            print("Specify directory containing .fits files to be imported.")
            directory=raw_input()
            load(directory,db_name)

        elif(inp == "filter"):

            print("Specify parameters to filter data. Each filter's parameters are inclusive of bounds, and should be separated by commas.")
            print("Pulsar name: 'name',(name)") #specify jname or bname?
            print("Originating observatory: 'o',(name of origin)")
            print("MJD: 'mjd',(lower bound),(upper bound)")
            print("Period: 'p',(lower bound),(upper bound)")
            print("Dispersion measure: 'dm',(lower bound),(upper bound)")
            print("Number of bins: 'bins',(lower bound),(upper bound)")

            filter(db_name)

        elif(inp == "exit"):
            print("Exiting program.")
            sys.exit()

        else:
            print("Command not valid. Please try again.")


def make(db_name):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    
    #try to create a new database in that name
    try:
        c.execute("""CREATE TABLE astrodata (
                name text,
                o text,
                mjd real,
                period real,
                dm real,
                bins integer
        )""")
        conn.commit()
        
    #catch an error if there is already a database with that name
    except sqlite3.Error as e:
        print("A database named " + db_name + " already exists. Please enter another name for the database, or 'o' to overwrite the existing one.")
        str = raw_input()
        
        #replace table if user wants to overwrite, but only if they are really sure
        if (str == "o"):
            
            print("ARE YOU SURE you want to overwrite your database? There's no going back. Type 'yes overwrite' to proceed, or another name for your database.")
            str = raw_input()
            
            if(str == "yes overwrite"):
                c.execute("DROP TABLE IF EXISTS astrodata")
                conn=sqlite3.connect(db_name)
                c=conn.cursor()
                c.execute("""CREATE TABLE astrodata (
                    name text,
                    o text,
                    mjd real,
                    period real,
                    dm real,
                    bins integer
                )""")
                conn.commit()
            else:
                make(str)
        else:
            make(str)
    conn.close()


def readFile(directory):
    hdulist = pyfits.open(directory)
    hdulist.verify('fix')
    header = hdulist[0].header
    header.set('filename', os.path.basename(directory))
    print(header)

    #only sample data right now.
    data=["B0919+06+22", "Arecibo", "53363.335636574076", "0.4305937417","27.3091", "128"]
    return data

def load(directory, db_name):
    dirpath = Path(directory)

    if(dirpath.is_dir()):
        print(".fits files will be loaded from " + directory + ".")
        loop = 0 #stop looping
        #load files
        conn=sqlite3.connect(db_name)
        c=conn.cursor()
        files=os.listdir(directory)
        i=0
        print("Reading these files:")
        while(i<len(files)):
            print("loopin")
            if "dyn.fit" not in files[i] and "dyn.fits" not in files[i]:
                del files[i]
                continue
            fname=directory+"/"+files[i]
            data=readFile(fname)
            print(data)
            command="INSERT INTO astrodata VALUES("+"'"+data[0]+"', "+"'"+data[1]+"', "+data[2]+", "+data[3]+", "+data[4]+", "+data[5]+")"
            c.execute(command)
            conn.commit()
            i+=1
        conn.close()

    else:
        print("Invalid directory. Type 'exit' to exit to the main menu or try again with a new input.")
        directory = raw_input()


def filter(db_name): #currently coded to only support one filter at a time
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    loop = 1 #looping query process
    q=raw_input()
    while (loop == 1):

        if(q == "exit"):
            loop = 0 #stop looping, exit to main menu
        else:
            print("oooooooooooo")
            queries = q.split(",")
            print(queries) #create list of parameters separated by commas
            if(queries[0] == "name"):
                pname = queries[1]
                print(pname)
                #process query
                command="SELECT * FROM astrodata WHERE name=\'"+pname+"\'"
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                break

            if(queries[0] == "o"):
                origin = queries[1]
                command="SELECT * FROM astrodata WHERE o=\'" + origin+"\'"
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                break

            if(queries[0] == "mjd"):
                low = queries[1]
                high = queries[2]
                command="SELECT * FROM astrodata WHERE mjd BETWEEN "+low+" AND "+high
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                    #process query
                break

            if(queries[0] == "p"):
                print("aaaaaaaaaa")
                low = queries[1]
                high = queries[2]
                #process query
                command="SELECT * FROM astrodata WHERE period BETWEEN "+low+" AND "+high
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                break

            if(queries[0] == "dm"):
                low = queries[1]
                high = queries[2]
                #process query
                command="SELECT * FROM astrodata WHERE dm BETWEEN "+low+" AND "+high
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                break

            if(queries[0] == "bins"):
                low = queries[1]
                high = queries[2]
                #process query
                command="SELECT * FROM astrodata WHERE bins BETWEEN "+low+" AND "+high
                c.execute(command)
                print(c.fetchall())
                conn.commit()
                break
            
            else:
                print("Invalid query. Type 'exit' to exit to the main menu or try again with a new input.")
                q = raw_input()
    conn.close()

#for main method on command line
if __name__ == "__main__": main()
