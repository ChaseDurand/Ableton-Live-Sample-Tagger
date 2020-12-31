import xml.etree.ElementTree as ET
import gzip
import shutil
import os
import glob
import collections

projects = []
projectsSet = set()
projectsAll = []

for file in glob.glob('/Users/chasedurand/Desktop/ZIPPED/**/*.als'):
    projects.append(file)

count = 1
total = len(projects)


for i in projects:
    destination = os.path.split(os.path.split(i)[0])[1] + ' - ' + os.path.splitext((os.path.split(i)[1]))[0]
    #destination = destination
    destination+='.xml'
    destination = '/Users/chasedurand/Desktop/UNZIPPED/' + destination
    #with gzip.open(i, 'r') as f_in, open(destination, 'wb') as f_out:
    #    shutil.copyfileobj(f_in, f_out)
    print('(',count,'/',total,')',destination)
    count += 1
'''
tree = ET.parse() #get XML file
root = tree.getroot()

sample_path = ""
sample_set = set()

for sample_element in root.iter('SampleRef'): #iterate over all sample references
        sample_path = ""
        for path in sample_element.find('FileRef').find('SearchHint').find('PathHint'):
                for path_element in path.iter('RelativePathElement'):
                        sample_path += '/' + path_element.get('Dir')
        for filename in sample_element.find('FileRef').iter('Name'):
                sample_path += '/' + filename.get('Value')
                sample_set.add(sample_path)
print("\n".join(sorted(sample_set)))
'''