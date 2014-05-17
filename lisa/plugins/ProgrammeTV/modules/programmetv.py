# -*- coding: UTF-8 -*-
import urllib
import xml.etree.ElementTree as ET
from datetime import date
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os


class ProgrammeTV(IPlugin):
    def __init__(self):
        super(ProgrammeTV, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "ProgrammeTV"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='programmetv',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext
    def getProgrammeTV(self, jsonInput):
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
                    programmetv_str = programmetv_str + self._('On ') +channelDict[child.attrib['channel']]\
                                      + self._(' at ') \
                                      + child.attrib['start'][8:10] + self._(' hour ') + child.attrib['start'][10:12]\
                                      + self._(' there is : ') + child.find('title').text + '. '
        return {"plugin": "programmetv",
                 "method": "getProgrammeTV",
                 "body": programmetv_str
        }

    def downloadProgrammeTV(self):
        url = "http://www.kazer.org/tvguide.xml?u=" + self.configuration_plugin['configuration']['user_id']
        if not os.path.exists('tmp/'+str(date.today())+'_programmetv.xml'):
            print self._("Downloading the tv program")
            import glob
            files=glob.glob('tmp/*_programmetv.xml')
            for filename in files:
                os.unlink(filename)
            urllib.urlretrieve(url,'tmp/'+str(date.today())+'_programmetv.xml')
        return "SUCCESS"