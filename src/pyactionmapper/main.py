import glob
from os.path import dirname
from pathlib import Path
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk

import collections

from structure import actionmaps
from util import VerticalScrolledFrame
class mapper():
    _file=Path(__file__)
    _module=dirname(_file.absolute())
    src_dir=dirname(_module)
    app_name="action mapper"
    # At some point should upgrade this to point to either the real mwll dir OR the mwll-code dir
    xml_dir=Path("{}/xml".format(dirname(src_dir)))
    xml_actionmap=f"{xml_dir}/default_actionmaps.xml"
    dtd_actionmap=f"{xml_dir}/actionmaps.dtd"
    xml_templates=glob.glob(f"{xml_dir}/actionmaps_*.xml")
    def __init__(self):
        # find the default action mapps, load and parse,
        #  pluck out the sections and their version. 
        self.load_default()
        # Get user directory?
        # hard code for now, OOO maybe it should be an input? allowing this "main" to be generic
        self.user_dir='phony/path/cry blarg/profile'
        #self.xml_user=Path(f"{self.user_dir}/actionmaps.xml")
        self.xml_user=Path(f"{mapper.xml_dir}/example_user.xml")
        self.user_map=self.load_map(self.xml_user)
        self.modified=False
        # todo: replicate backup dir behavior
        self.backup_dir=Path("f{self.user_dir}/backups")
        # todo, run backup when appropriate, probably on save, which should only be done if changed
        #self.backup()
        self.configure()
    def load_default(self):
        self.default_map=self.load_map(mapper.xml_actionmap)
        #print("Sections:{}".format(self.default_map.sections()))
    def load_map(self,xml_file):
        a_map=actionmaps()
        # lxml handling not complete because conversion from xml to dict is broken.
        # Decided that that is not a sufficient reason to worry about it.
        #a_map.populate(mapper.xml_actionmap, mapper.dtd_actionmap, parser='lxml')
        a_map.populate(xml_file, mapper.dtd_actionmap, parser='xmltodict')
        a_map.validate()
        return a_map
    def configure(self):
        # display graphical interface and allow user to do bits.
        # not sold on calling this method configure... but that is what the user would be doing.
        master = tk.Tk()
        master.title(mapper.app_name)
        tabControl = ttk.Notebook(master)
        tabControl.pack(expand=1, fill="both")
        section_names=self.default_map.section_names()
        gui_tabs=[None] * len(section_names)
        user_missing=[]
        # note: we use default actionmaps to handle ordering, so we use the section names from there.
        for s_idx,section_name in enumerate(section_names):
            gui_tabs[s_idx] = ttk.Frame(tabControl)
            # gui_tabs[s_idx] = VerticalScrolledFrame(tabControl)
            tabControl.add(gui_tabs[s_idx], text=section_name)
            #s_label.pack()
            row_n=0
            (u_section,map_s_idx)=self.user_map.get_section(section_name)
            (section,map_s_idx)=self.default_map.get_section(section_name)
            if u_section is None:
                section=u_section
                self.modified=True
            u_vers=u_section["version"]
            d_vers=section["version"]
            if u_vers != d_vers :
                u_section["version"]=d_vers
                self.modified=True
            s_label=ttk.Label(gui_tabs[s_idx], text=f"{section_name} vers={u_vers}")
            s_label.grid(column=0, row=row_n, padx=30, pady=30)
            row_n=row_n+1
            if section is None:
                print(f"Found no xml section {section_name}")
                continue
            col_st=0
            # note: we use default actionmaps to handle ordering, so we use the default section to set the action order, also we update user info from there.
            for a_idx,action in enumerate(section["action"]):
                try:
                    a_label=ttk.Label(gui_tabs[s_idx], text=action["display_name"])
                except KeyError as e:
                    a_label=ttk.Label(gui_tabs[s_idx], text=action["name"])
                a_label.grid(column=col_st, row=row_n, padx=0, pady=0)
                #a_label.pack()
                # get the user action
                (a,a_idx)=self.user_map.get_action(u_section,action["name"],True)
                if a is None:
                    user_missing.append((section_name,action["name"]))
                    a=action["key"]
                # bandaid when only one key is defined. This should be fixed during load instead of here.
                if type(a) is not list:
                    k=collections.OrderedDict()
                    k["name"]="null"
                    a=[a,k]
                    self.modified=True
                for col,key in enumerate(a):
                    k_name=key["name"]
                    if k_name == "null":
                        k_name=""
                    tvar=tk.IntVar()
                    tvar.set(k_name)
                    # Text entry is NOT the correct thing. It would probably be better to use a button which after clicking waited for user entered key.
                    e = tk.Entry(gui_tabs[s_idx],textvariable=tvar)
                    e.grid(row=row_n,column=col+col_st+1)
                    #e.pack()
                row_n=row_n+1
                # prevent row count from getting too long. 
                # This is to prevent a need for scrolling in the interface becuase that was hard to implement.
                if row_n > len(section["action"])/2 or row_n > 25:
                    col_st=col_st+3
                    row_n=1
        if len(user_missing):
            print("These actions were not defined by the user, and will be updated with the default values:")
            for missing in user_missing:
                print(missing)
        master.mainloop()
    def validate(self):
        # validate a loaded action map(WAIT.... no no no, that should be part of the actionap loading...)
        pass
    def compare(self,map1,map2=None):
        # with two actionmaps create comparrison data structure,...
        # display either through printout, OR through some kinda cool tree visualization.
        if map2 is None:
            map2=map1
            map1=self.default_map
        pass
    def backup(self):
        pass

if __name__ == '__main__':
    mapper=mapper()
    