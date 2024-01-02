import sys
from os.path import dirname
from pathlib import Path
import xmltodict
this_file=Path(__file__)
file_dir=dirname(this_file.absolute()   )
project_root=dirname(file_dir)
src_dir=Path(f"{project_root}/src")
xml_dir=Path(f"{project_root}/xml")
module_dir=Path(f"{src_dir}/pyactionmapper")

import glob

# This test is just a basic load and print of the baked in defaults
# uses custom dict class actionmaps to prove it works, and play around with its internal structure

sys.path.append(str(src_dir))
sys.path.append(str(module_dir))

from structure import actionmaps

#open the file
with open(f"{xml_dir}/default_actionmaps.xml","r") as fileptr:
    #read xml content from the file
    xml_content=fileptr.read()
    xml_content=xmltodict.parse(xml_content)

#print("XML content is:")
#print(xml_content)

#change xml format to ordered dict
my_ordered_dict=actionmaps(xml_content)
print("Ordered Dictionary is:")
print(my_ordered_dict)
print("First level:")
print(my_ordered_dict.keys())
print("Second level:")
print(my_ordered_dict["ActionMaps"].keys())
print("third level items: {}".format(len(my_ordered_dict["ActionMaps"]["actionmap"])))
print(my_ordered_dict["ActionMaps"]["actionmap"][0])
print("sections")
print(my_ordered_dict.sections())