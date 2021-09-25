from pathlib import Path
import xml.etree.ElementTree as ET
import gzip
from src.database import *
from src.xml import *
from src.xmp import *
'''
Functions for parsing ALS files.
'''


def getALSFiles(projectPathRoot):
    #Find all ALS files recursively in project directory and return as list
    #Ignores backup files
    alsFiles = []
    print('Finding .als files in', str(projectPathRoot))
    for alsFile in Path(projectPathRoot).glob('**/*.als'):
        if '/Backup/' not in str(alsFile):
            alsFiles.append(Path(alsFile))
    return alsFiles


def parseALS(alsFile, conn):
    #Finds, tags, and logs all sample references in a given ALS file
    cur = conn.cursor()
    #Process ALS and add samples to DB
    #If als is in DB and up to date, then no work is necessary
    if (alsInDB(alsFile, cur)):
        if (alsUpToDate(alsFile, cur)):
            print(alsFile.name, "is already up to date in DB.")
            return
    #ALS is not in DB or not up to date, need to process
    loggedSamples = {}  #Logged samples for this project per script execution
    projectID = addALStoDB(alsFile, cur)
    #Convert to XML and get all sample references
    xmlFile = gzip.open(alsFile, 'r')
    root = (ET.parse(xmlFile)).getroot()

    for sample_element in root.iter('SampleRef'):
        for fileRef in sample_element.findall('FileRef'):
            #Relative path must be used if HasRelativePath="true" and RelativePathType="3"
            if fileRef.find('HasRelativePath').get(
                    'Value') == "true" and fileRef.find(
                        'RelativePathType').get('Value') == "3":
                samplePath = getRelativePath(fileRef, alsFile)

            else:
                samplePath = getAbsolutePath(fileRef)
            if samplePath == None:
                continue
            #If path is not new to this project, then we don't need to attempt tag+log+mapping
            #If this is our first time seeing this project-sample combo this execution, attempt tag+log+map
            if samplePath not in loggedSamples:
                loggedSamples[samplePath] = True
                #tag XMP
                tagSample(samplePath)
                #add to sample table
                sampleID = addSampletoDB(samplePath, cur)
                #add to mapping table
                addProjectSampleMapping(projectID, sampleID, cur)
    conn.commit()
    cur.close()
    return