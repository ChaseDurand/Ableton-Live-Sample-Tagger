import xml.etree.ElementTree as ET
from sqlite3 import Error
from pathlib import Path
from ALST.als import *
from ALST.database import *

###########################################
# Promt user for path to Ableton Live Projects (and SQLite database)
while True:
    projectPathRoot = Path(input("Enter Ableton Live Projects directory: "))
    if projectPathRoot.is_dir():
        break
    else:
        print(projectPathRoot, " is not a valid path!")

conn = initializeDatabase(projectPathRoot)
alsFiles = getALSFiles(projectPathRoot)
print("Found", len(alsFiles), ".als files")
for als in alsFiles:
    parseALS(als, conn)
#TODO need to go through all samples and tag if needed
#Samples previously not tagged but logged could now be accessible
conn.close
exit()
