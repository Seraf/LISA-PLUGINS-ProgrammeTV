# -*- coding: UTF-8 -*-
import urllib, json
import xml.etree.ElementTree as ET
from datetime import date
import os, inspect
from pymongo import MongoClient
from lisa import configuration
import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='programmetv', localedir=path, languages=[configuration['lang']]).ugettext

class ProgrammeTV:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'],
                            self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "ProgrammeTV"})

    def getProgrammeTV(self):
        self.downloadProgrammeTV()
        programmetv = ET.parse('tmp/'+str(date.today())+'_programmetv.xml').getroot()

        channelDict = {}
        programmetv_str = ""
        for child in programmetv:
            if child.tag == "channel":
                channelDict[child.attrib['id']] = child.find('display-name').text
            if child.tag == "programme":
                if date.today().strftime("%Y%m%d")+"2045" <= child.attrib['start'][:12] and \
                                        date.today().strftime("%Y%m%d")+"2200" > child.attrib['start'][:12]:
                    programmetv_str = programmetv_str + _('On ') +channelDict[child.attrib['channel']] + _(' at ')     \
                                      + child.attrib['start'][8:10] + _(' hour ') + child.attrib['start'][10:12]       \
                                      + _(' there is : ') + child.find('title').text + '. '
        return json.dumps({"plugin": "programmetv","method": "getProgrammeTV", "body": programmetv_str})

    def downloadProgrammeTV(self):
        url = "http://www.kazer.org/tvguide.xml?u=" + self.configuration['configuration']['user_id']
        if not os.path.exists('tmp/'+str(date.today())+'_programmetv.xml'):
            print _("Downloading the tv program")
            import glob
            files=glob.glob('tmp/*_programmetv.xml')
            for filename in files:
                os.unlink(filename)
            urllib.urlretrieve(url,'tmp/'+str(date.today())+'_programmetv.xml')
        return "SUCCESS"