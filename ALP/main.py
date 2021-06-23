import xml.etree.ElementTree as ET
import gzip
import shutil
import os
from xmp_tagger import xmp_tag
from natsort import natsorted
import sqlite3
from sqlite3 import Error
from pathlib import Path
import tempfile


def insertProject(projectPath):

    with conn:
        cur.execute(
            "INSERT INTO projects (projectName, setName, setPath, setModDate) VALUES (?,?,?,?)",
            (str(projectPath.parent.name), str(projectPath.name),
             str(projectPath), projectPath.stat().st_mtime))
        return cur.lastrowid


def findProjects(projectPathRoot):
    #Finds all new or newly modified projects in a directory
    print('Finding .als files.')
    for file in Path(projectPathRoot).glob(
            '**/*.als'):  # Find all als files in all subdirectories
        if '/Backup/' not in str(
                file
        ):  # Filter to ignore backup als files and add remaining to list
            #If project is not in database, add
            cur = conn.cursor()
            result = cur.execute(
                'SELECT * FROM projects WHERE projectName= ? AND setName=?;',
                (str(file.parent.name), str(file.name)))
            if (len(result.fetchall()) == 0):
                #Add to database
                print("Inserting and parsing", file)
                rowID = insertProject(file)
                result = cur.execute(
                    'SELECT * FROM projects WHERE projectID= ?;', (rowID, ))
                logProjectSamples(result.fetchone())
            else:
                #already in database
                #Need to check if current date modified != logged date modified
                result = cur.execute(
                    'SELECT * FROM projects WHERE projectName= ? AND setName=?;',
                    (str(file.parent.name), str(file.name)))
                if (file.stat().st_mtime != result.fetchone()['setModDate']):
                    #if modified date doesn't match
                    #update mod date
                    print("Updating", file)
                    logProjectSamples(result.fetchone())
                else:
                    #not modified, no work required
                    print("Already up to date", file)
            cur.close()
            conn.commit()


def logProjectSamples(projectRow):
    global cur
    cur.close()
    global conn
    cur = conn.cursor()
    #For each row in project table, create XML file and get all sample paths.
    #Log samples in the sample and mapping tables
    xmlPath = convertToXML(projectRow)
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    for sample_element in root.iter('SampleRef'):
        for data_tag in sample_element.iter('FileRef'):
            hex = data_tag.find('Data').text

            try:
                hex = ''.join(
                    hex.split())  # Strip newlines and whitespace from hex
                path = hex2path(hex)
                #Check if found path already exists in the sample table
                cur.close()
                cur = conn.cursor()
                result = cur.execute('SELECT * FROM samples WHERE path= ?;',
                                     (str(path), ))
                #If path is new, add to sample table
                conn.commit()
                if (len(result.fetchall()) == 0):
                    #Sample is new
                    sampleName = data_tag.find('Name').get('Value')
                    cur.close()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO samples (sampleName, path, found) VALUES (?,?,?)",
                        (sampleName, str(path), path.exists()))
                    conn.commit
                    tagSample(str(path))
                cur.close()
                cur = conn.cursor()
                #Get sample ID from path
                result = cur.execute('SELECT * FROM samples WHERE path = ?;',
                                     (str(path), ))
                conn.commit()
                sampleID = result.fetchone()['sampleID']
                #Check if mapping already exists in the mapping table
                cur.close()
                cur = conn.cursor()
                result = cur.execute(
                    'SELECT * FROM projectSampleMapping WHERE projectID = ? AND sampleID = ?;',
                    (projectRow['projectID'], sampleID))
                conn.commit()
                #If mapping is new, add to mapping table
                if (len(result.fetchall()) == 0):
                    cur.close()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO projectSampleMapping (projectID, sampleID) VALUES (?,?)",
                        (projectRow['projectID'], sampleID))
                    conn.commit
            except AttributeError:
                print('Could not parse path')


def convertToXML(projectRow):
    #For each row in project table, convert als file to xml
    alsPath = projectRow['setPath']
    #Construct destination XML file name 'ProjectName - SetName.xml'
    xmlPath = xmlPathRoot.joinpath(projectRow['projectName'] + ' - ' +
                                   projectRow['setName'] + '.xml')
    with gzip.open(alsPath, 'r') as f_in, open(xmlPath, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return xmlPath


#Takes given hex data chunk from ALS xml file and returns filepath Path object
def hex2path(data):
    path = bytearray.fromhex(data)
    found_path = ''
    #Finds : which looks to be uniquely found in the sample path
    #I should probably figure out what the rest of the hex is and how it's structured
    #This implementation ignores volumes, which appears to be stored early in the hex, so I'm unsure how it handles samples from another volume, such as a USB drive
    i = 0
    while i < len(path):
        if (path[i] != 0x00) and (path[i] != 0xFF):
            first_index = i
            length = path[i]
            offset = 1
            found_string = ''
            while (offset <= length) and (path[first_index + offset] !=
                                          0x00) and (path[first_index + offset]
                                                     != 0xFF):
                if (first_index + offset) == len(path):
                    print('woah now')
                found_string += chr(path[first_index + offset])
                offset += 1
            if offset == length + 1:
                #possible valid string
                if found_string != '/':
                    found_path = found_string
            i = first_index + offset
        i += 1
    found_path = '/' + found_path
    return Path(found_path)


def initializeDatabase(db_file):
    #If database doesn't exit, create database with tables.
    #Regardless, return connection to database.
    db_file = db_file.joinpath(str(db_file) + '/ALST.db')
    print(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    #Check if database with tables already exists
    try:
        cursor.execute("""CREATE TABLE projects (
                    projectID INTEGER PRIMARY KEY,
                    projectName text,
                    setName text,
                    setPath text,
                    setModDate integer
                )""")
    except Error as e:
        print(e)
        print("Database already exists.")
        return conn
    cursor.execute("""CREATE TABLE samples (
                sampleID INTEGER PRIMARY KEY,
                sampleName text,
                path text,
                found integer
            )""")

    cursor.execute("""CREATE TABLE projectSampleMapping (
                mappingID INTEGER PRIMARY KEY,
                projectID integer,
                sampleID integer
            )""")
    cursor.close()
    conn.commit
    return conn


#Tags a single file passed as an input
def tagSample(path_input):

    #TODO refresh this entire logic
    #Change paths to pathlib
    filepath = os.path.splitext((os.path.split(path_input)[0]))[0]
    file = os.path.splitext(
        (os.path.split(path_input)[1]))[0] + os.path.splitext(
            (os.path.split(path_input)[1]))[1]

    if not os.path.isdir(filepath + '/Ableton Folder Info/'):
        #need to create folder
        Path(filepath + '/Ableton Folder Info').mkdir(parents=True,
                                                      exist_ok=True)
    if not os.path.isfile(filepath + '/Ableton Folder Info/' +
                          'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp'):
        #need to create .xmp file
        xmp_create(filepath)

    f = open(
        filepath + '/Ableton Folder Info/' +
        'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp', 'r')
    contents = f.readlines()
    f.close()

    #Have start and stop ranges for existing samples and tags
    #For sample, need to check if existing
    #Search lines for sample
    count = 0
    file_line = 0
    for line in contents:
        #lines.append(line)
        if file in line:
            file_line = count
        count += 1
    #If existing, need to check if tag 1 exists
    if file_line != 0:
        if '<rdf:li>1</rdf:li>' in contents[file_line + 3]:
            #sample is already tagged 1
            print('     Existing tag on', file)
        else:
            value = '''                            <rdf:li>1</rdf:li>
'''
            contents.insert(file_line + 3, value)
            print('     Tagged', file)
    #If not existing, add base sample structure and tag 1
    else:
        value = """               <rdf:li rdf:parseType="Resource">
                   <ablFR:filePath>""" + file + """</ablFR:filePath>
                      <ablFR:colors>
                         <rdf:Bag>
                            <rdf:li>1</rdf:li>
                         </rdf:Bag>
                    </ablFR:colors>
                 </rdf:li>
"""
        contents.insert(11, value)
        print('     Tagged', file)

    f = open(
        filepath + '/Ableton Folder Info/' +
        'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp', 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()
    return ()


#Creates a barebones xmp file in given folder with no tags
#CreatorTool, CreateDate, and MetadataDate are not accurate
def xmp_create(path_input):
    #TODO refresh
    #Change to pathlib
    f = open(
        path_input + '/Ableton Folder Info/' +
        'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp', "x")
    f.write("""<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.6.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:ablFR="https://ns.ableton.com/xmp/fs-resources/1.0/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/">
         <dc:format>application/vnd.ableton.folder</dc:format>
         <ablFR:resource>folder</ablFR:resource>
         <ablFR:platform>mac</ablFR:platform>
         <ablFR:items>
            <rdf:Bag>
            </rdf:Bag>
         </ablFR:items>
         <xmp:CreatorTool>Updated by Ableton Index 10.1.30</xmp:CreatorTool>
         <xmp:CreateDate>2021-01-19T21:39:24-05:00</xmp:CreateDate>
         <xmp:MetadataDate>2021-01-21T07:55:28-05:00</xmp:MetadataDate>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>""")
    f.close()
    return ()


###########################################
# Promt user for path to Ableton Live Projects (and SQLite database)
while True:
    projectPathRoot = Path(input("Enter Ableton Live Projects directory: "))
    if projectPathRoot.is_dir():
        break
    else:
        print(projectPathRoot, " is not a valid path!")

conn = initializeDatabase(projectPathRoot)
cur = conn.cursor()

temp_dir = tempfile.TemporaryDirectory()
xmlPathRoot = Path(temp_dir.name)
print(temp_dir.name)
findProjects(projectPathRoot)

conn.close()
exit()