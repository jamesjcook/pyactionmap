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

xml_path=Path(f"{xml_dir}/actionmaps_default_2.xml")
xml_path=Path(f"{xml_dir}/actionmaps_invictus_2.xml")
xml_path=Path(f"{xml_dir}/default_actionmaps.xml")
dtd_path=Path(f"{xml_dir}/actionmaps.dtd")
#xml_path=path(f"{xml_dir}/test_for_validation.xml")
for f in [xml_path,dtd_path]:
    if not f.is_file():
        raise FileNotFoundError(f)

#open the file
with open(xml_path,"r") as fileptr:
    #read xml content from the file
    xml_content= fileptr.read()
    my_ordered_dict=xmltodict.parse(xml_content)

#print("XML content is:")
#print(xml_content)
#change xml format to ordered dict
from lxml import etree
parser = etree.XMLParser(dtd_validation=False)
dtd=etree.DTD(dtd_path)
tree = etree.parse(xml_path, parser)
if not dtd.validate(tree):
    raise ValueError('XML DTD validation failed Errors:{}'.format(
    str(dtd.error_log.filter_from_errors())))
else:
    print("Validation passed!")

#fail
#print(tree["ActionMaps"])
# works
#print( "{}".format(etree.tostring(tree,pretty_print=True)) )
#print( "{}".format(etree.tostring(tree.getroot(),pretty_print=True)) )
root_e=tree.getroot()
n=root_e.attrib

# n=root_e.getitems
print( "{}".format(root_e) )


