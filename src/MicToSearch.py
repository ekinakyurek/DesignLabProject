# -*- coding: utf-8 -*-
import time
from WebSearch import *
from MicToText import *

class MicToSearch:
    def __init__(self,morph_location="../morph/trmorph.fst",record_folder="../records/",debug=False):
        self.mictotext = MicToText(morph_location=morph_location,record_folder=record_folder, debug=debug)
        self.websearch = WebSearch(debug=debug)
    def startrecording(self):
        self.mictotext.start()
    def stoprecording(self):
        self.mictotext.stop()
    def searchlastspeech(self):
        text = self.mictotext.reader()
        return self.websearch.starter(text,False,None,None)

#
# a =  web_search.WebSearch()
# test_input = "ekin konulsa da güneş balçıkla ekin yasak,Noun konul,Noun da,Other güneş,Noun balçık,Noun ekin,Noun";
# a.starter(test_input, True, None, None)
