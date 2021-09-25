from pathlib import Path
'''
Functions for parsing and writing XMP files.
'''

#Barebones XMP file template
#CreatorTool, CreateDate, and MetadataDate are not accurate
#TODO add custom creator tool and date info
xmpTemplate = """<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.6.0">
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
</x:xmpmeta>"""

#XMP directory+file structure
#TODO figure out xmp filename meaning
xmpFilepathTail = Path('Ableton Folder Info',
                       'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp')


def createXMP(path_input):
    #Creates a barebones xmp file in given folder with no tags
    xmpPath = Path.joinpath(path_input, xmpFilepathTail)
    f = open(str(xmpPath), "x")
    f.write(xmpTemplate)
    f.close()
    return


def tagSample(path_input):
    #If sample does not have XMP tag, tag it
    samplePath = path_input.parent
    sample = path_input.name

    #Check for folder and XMP file, creating if not found
    if not (samplePath.joinpath(str(samplePath) +
                                'Ableton Folder Info')).exists():
        #TODO need to check if we can mkdir (volume might be removed)
        #If not, return false
        if path_input.exists() != True:
            print('     Unable to tag', str(sample), 'at', str(samplePath))
            return
        else:
            Path(str(samplePath) + '/Ableton Folder Info').mkdir(parents=True,
                                                                 exist_ok=True)

    if not (samplePath.joinpath(str(xmpFilepathTail))).exists():
        createXMP(samplePath)

    f = open(str(samplePath.joinpath(str(xmpFilepathTail))), 'r')
    contents = f.readlines()
    f.close()

    #TODO improve this parsing
    #Have start and stop ranges for existing samples and tags
    #For sample, need to check if existing
    #Search lines for sample
    count = 0
    file_line = 0
    for line in contents:
        #lines.append(line)
        if str(sample) in line:
            file_line = count
        count += 1
    #If sample appears in XMP file, need to check if tag 1 exists and add if needed
    if file_line != 0:
        if '<rdf:li>1</rdf:li>' in contents[file_line + 3]:
            print('     Existing tag on', str(sample))
        else:
            value = '''                            <rdf:li>1</rdf:li>
'''
            contents.insert(file_line + 3, value)
            print('     Tagged', str(sample))
    #If sample doesn't appear in XMP file, add base sample structure and tag 1
    else:
        value = """               <rdf:li rdf:parseType="Resource">
                   <ablFR:filePath>""" + sample + """</ablFR:filePath>
                      <ablFR:colors>
                         <rdf:Bag>
                            <rdf:li>1</rdf:li>
                         </rdf:Bag>
                    </ablFR:colors>
                 </rdf:li>
"""
        contents.insert(11, value)
        print('     Tagged', str(sample))

    f = open(
        str(samplePath) + '/Ableton Folder Info/' +
        'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp', 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()
    return