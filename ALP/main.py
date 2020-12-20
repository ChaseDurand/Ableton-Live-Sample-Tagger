import xml.etree.ElementTree as ET

#tree = ET.parse('/Users/chasedurand/Desktop/SET1.xml') #get XML file
tree = ET.parse('/Users/chasedurand/Desktop/DNB.xml') #get XML file
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