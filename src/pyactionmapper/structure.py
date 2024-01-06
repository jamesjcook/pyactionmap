import collections
from pathlib import Path
import os

def elem2dict(node, attributes=True):
    """
    Convert an lxml.etree node tree into a dict.
    from https://gist.github.com/jacobian/795571
    """
    result = {}
    if attributes:
        for item in node.attrib.items():
            #for item in node.items():
            print("Add {} with {}".format(key,result[key]))
            key, result[key] = item

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:
            if type(result[key]) is list:
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = value
    return result


def elem2dict2019(node):
    """
    Convert an lxml.etree node tree into a dict.
    from https://gist.github.com/jacobian/795571 via https://stackoverflow.com/a/66103841
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict2019(element)
        if key in result:

            
            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result

# classes arranged from least to most specific.
class profile():
    def __init__(self,profile_dir,test_mode=False):
        self.modified = False
        self.dir=profile_dir
        self.name=profile.get_profile_name(self.dir)
        self.xml_actionmaps=Path(f"{self.dir}/actionmaps.xml")
        self.actionmaps=actionmaps()
        self.backup_dir=Path(f"{self.dir}/backups")

    def get_profile_name(profile_dir):
        # placeholder function to get the profile name given a profile dir.
        return os.path.basename(profile_dir)

    def load_actionmaps(self,validator=None):
        # this NOT loaded on init because we might want to slip in an alternate xml_path for xml_actionmaps
        self.actionmaps=actionmaps()
        self.actionmaps.load(self.xml_actionmaps,validator)
    def backup_actionmaps(self):
        pass
    def save_actionmaps(self):
        self.backup_actionmaps()
        self.actionmaps.save()
    def restore_backup(profile_dir,xml_file):
        # get date on current xml,
        # move currnet xml to backus/date
        # copy xml_file to self.xml_actionmaps
        pass

class actionmaps(collections.OrderedDict):
    top_key="ActionMaps"
    main_key="actionmap"
    # attr_prefix='@'
    attr_prefix=''
    def __init__(self, *args, **kwargs):
        super(actionmaps, self).__init__(*args, **kwargs)
        self.order=None
    def validate(self):
        # quasi placeholder 
        top_level=list(self.keys())
        if len(top_level) == 1: 
            top_level=top_level[0]
        else:
            raise ValueError(f"Wrong number of Top-level values in XML. Found {len(top_level)}/1.")
        if top_level != actionmaps.top_key:
            raise ValueError(f"Invalid Top-level of XML not expected value '{actionmaps.top_key}' != '{top_level}'")
    def get_section(self, lookup, missing_ok=False):
        # find section with the name, raise ValueError if not found.
        # can use missing_ok=True to avoid error
        for idx,section in enumerate(self[actionmaps.top_key]["actionmap"]):
            if lookup == section["name"]:
                return section,idx
        if not missing_ok:
            raise ValueError(f"no {lookup} found")
        return None,-1
    def get_action(self, section, lookup, missing_ok=False):
        # check section for the name, raise ValueError if not found.
        # sectoin can either be the section or the name of the section
        # can use missing_ok=True to avoid error
        if type(section) == str:
            section,s_idx=self.get_section(section)
        for idx,a in enumerate(section["action"]):
            if lookup == a["name"]:
                return a,idx
        if not missing_ok:
            raise ValueError(f"no {lookup} found in {section['name']}")
        return None,-1
    def load(self, xml_file,validator=None):
        # lxml handling not complete because conversion from xml to dict is broken.
        # Decided that that is not a sufficient reason to worry about it.
        #self.populate(mapper.xml_actionmap, mapper.dtd_actionmap, parser='lxml')
        self.populate(xml_file, validator=validator, parser='xmltodict')
        self.validate()
    def save(self):
        pass
    def section_names(self):
        # get names of all sections
        vals = [ section["{}name".format(actionmaps.attr_prefix)] for section in self[actionmaps.top_key][actionmaps.main_key] ]
        return vals
    def populate(self,input,validator=None,parser='xmltodict'):
        if parser == 'xmltodict':
            import xmltodict
            with open(input) as map_h:
                # This will fail instantly IF malformed xml
                odict=xmltodict.parse(map_h.read(),
                    attr_prefix=actionmaps.attr_prefix)
        elif parser == 'lxml':
            from lxml import etree
            parser = etree.XMLParser(dtd_validation=False)
            tree = etree.parse(input, parser)
            if validator is not None:
                dtd=etree.DTD(validator)
                if not dtd.validate(tree):
                    raise ValueError('XML DTD validation failed Errors:{}'.format(
                    str(dtd.error_log.filter_from_errors())))
                else:
                    print("Validation passed!")
            # DERP... ned to unwrap to get into the ordered dict
            #print(tree)
            odict=elem2dict(tree.getroot())
        else:
            raise ValueError(f"Unrecognized xml parser selection {parser}")
        if "visible" in odict[actionmaps.top_key].keys():
            self.order=odict[actionmaps.top_key]["visible"]["map"]
            #print("Required actionmap order; {}".format(self.order))
            list_of_maps=[None] * len(self.order)
            for map in odict[actionmaps.top_key]["actionmap"]:
                try:
                    idx=self.order.index(map["{}name".format(actionmaps.attr_prefix)])
                except ValueError as e:
                    idx=-1
                if 0 < idx:
                    list_of_maps[idx]=map

            while(None in list_of_maps):
                list_of_maps.remove(None)
            odict[actionmaps.top_key]["actionmap"]=list_of_maps
            #odict=collections.OrderedDict((k, odict[k]) for k in self.order)

        self.update(odict)

class Action:
    # unused class for handling actions
    def __init__(self, *keys, onPress=False, onRelease=False, onHold=False, 
        retriggerable=False, consoleCmd=False, noModifiers=False, always=False):
        self.onPress = onPress
        self.onRelease = onRelease
        self.onHold = onHold
        self.retriggerable = retriggerable
        self.consoleCmd = consoleCmd
        self.noModifiers = noModifiers
        self.always = always
        self.keys = keys
        

    def getAttrs(self):
        return (self.onPress, self.onRelease, self.onHold, self.retriggerable,
         self.consoleCmd, self.noModifiers, self.always)

    def getKeys(self):
        return tuple(self.keys)
