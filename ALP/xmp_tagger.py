import os
from pathlib import Path

#test_path = '/Users/chasedurand/Desktop/test folder/Yea_Dilla vox.wav'
#test_path = '/Users/chasedurand/Desktop/asdf.wav'

#Tags a single file passed as an input
def xmp_tag(path_input):
    filepath = os.path.splitext((os.path.split(path_input)[0]))[0]
    file = os.path.splitext((os.path.split(path_input)[1]))[0] + os.path.splitext((os.path.split(path_input)[1]))[1]

    if not os.path.isdir(filepath + '/Ableton Folder Info/'):
        #need to create folder
        Path(filepath + '/Ableton Folder Info').mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(filepath + '/Ableton Folder Info/' + 'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp'):
        #need to create .xmp file
        xmp_create(filepath)

    f = open(filepath + '/Ableton Folder Info/' + 'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp','r')
    contents = f.readlines()
    f.close()

    '''
    lines = []
    line_index = []
    count = 0

    for line in contents:
        lines.append(line)
        if "ablFR:items" in line:
            line_index.append(count)
        count += 1

    start_index = 0
    stop_index = 0

    if len(line_index) != 2:
        print("Error: invalid xmp structure!")
    else:
        start_index = line_index[0]
        stop_index = line_index[1]
    print(start_index)
    print(stop_index)
    '''

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
        if '<rdf:li>1</rdf:li>' in contents[file_line+3]:
            #sample is already tagged 1
            print(file,'is already tagged')
        else:
            value='''                            <rdf:li>1</rdf:li>
'''
            contents.insert(file_line+3,value)
            print(file,'tagged')
    #If not existing, add base sample structure and tag 1
    else:
        value="""               <rdf:li rdf:parseType="Resource">
                   <ablFR:filePath>"""+file+"""</ablFR:filePath>
                      <ablFR:colors>
                         <rdf:Bag>
                            <rdf:li>1</rdf:li>
                         </rdf:Bag>
                    </ablFR:colors>
                 </rdf:li>
"""
        contents.insert(11,value)
        print(file, 'tagged')

    f = open(filepath + '/Ableton Folder Info/' + 'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp', 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()
    return()

#Creates a barebones xmp file in given folder with no tags
#CreatorTool, CreateDate, and MetadataDate are not accurate
def xmp_create(path_input):
    f = open(path_input + '/Ableton Folder Info/' + 'dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp',"x")
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
    return()

#xmp_tag(test_path)
#xmp_create('/Users/chasedurand/Desktop/')

'''
count = start_index
while count < stop_index:
    if "hype builder 1.wav" in lines[count]:
        print(count)
    count += 1
    
'''