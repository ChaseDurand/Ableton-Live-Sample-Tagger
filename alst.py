import sys
import concurrent.futures
from pathlib import Path
from src.als import *
from src.database import *

def main():
    # Confirm only arguments are script+directory
    if(len(sys.argv) != 2):
        print("Error: Expected 1 argument but found",len(sys.argv)-1)
        if(len(sys.argv) == 1):
            print("Please provide Ableton Live Projects directory as argument!")
        exit(1)

    # Verify path is directory
    projectPathRoot = Path(sys.argv[1])
    if projectPathRoot.is_dir() == False:
        print("Error: ", projectPathRoot, " is not a valid path!")
        exit(1)

    alsFiles = getALSFiles(projectPathRoot)
    print("Found", len(alsFiles), ".als files")

    conn = initializeDatabase(projectPathRoot)
    # Updated function call to use multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda alsFile: parseALS(alsFile, projectPathRoot), alsFiles)

    # TODO need to go through all samples and tag if needed
    # Samples previously not tagged but logged could now be accessible
    conn.close()
    exit()

if __name__ == '__main__':
    main()
