#A program that stores a SQLite database of pulsar dynamic spectrum data.
#Takes user queries and behaves accordingly. [more desc here]
from __builtin__ import raw_input
import sys

#fields
dataSize = 0 #the number of files in the database, initialize to 0


#main method
def main():
    
    print("Welcome to the pulsar database!")
    print("Your database currently contains " + str(dataSize) + " files.")
    
    while(1>0): #loop querying forever

        print("What would you like to do?")
        print("(load) - Load new data into the database")
        print("(filter) - Filter data with specific parameters")
        print("(exit) - Exit the program")
    
        #take in user's input
        inp = raw_input()
        
        #cases
        if (inp == "load"):
            print("Specify directory containing .fits files to be imported.")
            load(raw_input()) 
        
        elif(inp == "filter"):
            
            print("Specify parameters to filter data. Each filter's parameters are inclusive of bounds, and should be separated by commas.")
            print("Pulsar name: 'name',(name)") #specify jname or bname?
            print("Originating observatory: 'o',(name of origin)")
            print("MJD: 'mjd',(lower bound),(upper bound)")
            print("Period: 'p',(lower bound),(upper bound)")
            print("Dispersion measure: 'dm',(lower bound),(upper bound)")
            print("Number of bins: 'bins',(lower bound),(upper bound)")
            
            filter(raw_input())
            
        elif(inp == "exit"):
            print("Exiting program.")
            sys.exit()
            
        else:
            print("Command not valid. Please try again.")
    
    
def load(directory):
    
    loop = 1 #looping the query process
    
    while(loop == 1):
        valid = 1 #validity of directory
        #check validity of directory
        
        if(valid == 1):
            print(".fits files will be loaded from " + directory + ".")
            loop = 0 #stop looping
            #do the loading
        elif(directory == "exit"):
            loop = 0 #stop looking, exit to main menu
        else:
            print("Invalid directory. Type 'exit' to exit to the main menu or try again with a new input.")
            directory = raw_input()

def filter(q): #currently coded to only support one filter at a time
    
    loop = 1 #looping query process
    
    while (loop == 1):
        
        if(q == "exit"):
            loop = 0 #stop looping, exit to main menu
        else:
            queries = q.split(",") #create list of parameters separated by commas

            if(len(queries) == 2):
                if(queries[0] == "name"):
                    pname = queries[1]
                    #process query
                    
                if(queries[0] == "o"):
                    origin = queries[1]
            
            elif(len(queries) == 3):
                if(queries[0] == "mjd"):
                    low = queries[1]
                    high = queries[2]
                    #process query
                    
                if(queries[0] == "p"):
                    low = queries[1]
                    high = queries[2]
                    #process query
                    
                if(queries[0] == "dm"):
                    low = queries[1]
                    high = queries[2]
                    #process query
                    
                if(queries[0] == "bins"):
                    low = queries[1]
                    high = queries[2]
                    #process query
                else:
                        print("Invalid query. Type 'exit' to exit to the main menu or try again with a new input.")
                        q = raw_input()
        
        
#for main method on command line
if __name__ == "__main__": main()
    