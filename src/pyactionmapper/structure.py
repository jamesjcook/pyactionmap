import collections

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
            if lookup in section["name"]:
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
            if lookup in a["name"]:
                return a,idx
        if not missing_ok:
            raise ValueError(f"no {lookup} found in {section['name']}")
        return None,-1
    def section_names(self):
        # get names of all sections
        vals = [ section["{}name".format(actionmaps.attr_prefix)] for section in self[actionmaps.top_key][actionmaps.main_key] ]
        return vals
    def populate(self,input,validator=None,parser='xmltodict'):
        if parser == 'xmltodict':
            import xmltodict
            with open(input) as defmap:
                # This will fail instantly IF malformed xml
                odict=xmltodict.parse(defmap.read(),
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
