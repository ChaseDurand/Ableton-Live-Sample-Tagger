import xml.etree.ElementTree as ET
print('Hello World!\n') #Really breaking new ground here

tree = ET.parse('/Users/chasedurand/Desktop/SET1.xml')
root = tree.getroot()

'''
for LiveSet in root:
        print(LiveSet.attrib)
        for child in LiveSet:
                print(child.attrib, child.tag)
'''

for sample_element in root.iter('SampleRef'):
        for path_element in sample_element.iter('PathHint'):
                for path in path_element.iter('RelativePathElement'):
                        print(path.get('Dir'),'/',sep='',end='')
        print(sample_element.find('FileRef').find('Name').get('Value'))