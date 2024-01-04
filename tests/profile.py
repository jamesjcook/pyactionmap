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
dtd_actionmap=Path(f"{xml_dir}/actionmaps.dtd")

# This test is just a basic load and print of the baked in defaults
# uses custom dict class actionmaps to prove it works, and play around with its internal structure

sys.path.append(str(src_dir))
sys.path.append(str(module_dir))

from structure import profile,actionmaps


test_profile=profile(xml_dir,test_mode=True)
test_profile.xml_actionmaps=Path(f"{xml_dir}/example_user.xml")
test_profile.load_actionmaps(dtd_actionmap)
print(test_profile.actionmaps.section_names())
