from pathlib import Path
import xml.etree.ElementTree as ET
import gzip
from src.database import *
from src.xml import *
from src.xmp import *
'''
Functions for parsing ALS files.
'''


def getAbsolutePath(fileRef):
    data_element = fileRef.find('Data')
    if data_element is not None and data_element.text is not None:
        file_name = data_element.text.strip()
        if len(file_name) <= 255:
            absolutePath = Path(file_name)
            if absolutePath.is_file():
                return str(absolutePath)
    return None

def getALSFiles(projectPathRoot):
    alsFiles = []
    print('Finding .als files in', str(projectPathRoot))
    for alsFile in Path(projectPathRoot).glob('**/*.als'):
        if '/Backup/' not in str(alsFile):
            alsFiles.append(Path(alsFile))
    return alsFiles

def addALStoDB(als, cur):
    cur.execute('''
        INSERT OR REPLACE INTO projects (projectPath, projectName, lastModified)
        VALUES (?, ?, ?);
        ''', (str(als), als.name, als.stat().st_mtime))
    cur.execute('''
        SELECT projectID FROM projects WHERE projectPath = ?;
    ''', (str(als),))
    result = cur.fetchone()
    if result is not None:
        return result['projectID']
    else:
        return None

def parseALS(alsFile, conn):
    cur = conn.cursor()
    if (alsInDB(alsFile, cur)):
        if (alsUpToDate(alsFile, cur)):
            print(alsFile.name, "is already up to date in DB.")
            return
    loggedSamples = {}
    projectID = addALStoDB(alsFile, cur)
    xmlFile = gzip.open(alsFile, 'r')
    root = (ET.parse(xmlFile)).getroot()

    for sample_element in root.iter('SampleRef'):
        for fileRef in sample_element.findall('FileRef'):
            has_relative_path_element = fileRef.find('HasRelativePath')
            relative_path_type_element = fileRef.find('RelativePathType')
            if (has_relative_path_element is not None and 
                has_relative_path_element.get('Value') == "true" and
                relative_path_type_element is not None and
                relative_path_type_element.get('Value') == "3"):
                samplePath = getRelativePath(fileRef, alsFile)
            else:
                samplePath = getAbsolutePath(fileRef)
            if samplePath == None:
                continue
            if samplePath not in loggedSamples:
                loggedSamples[samplePath] = True
                tagSample(samplePath)
                sampleID = addSampletoDB(samplePath, cur)
                addProjectSampleMapping(projectID, sampleID, cur)
    conn.commit()
    cur.close()
    return