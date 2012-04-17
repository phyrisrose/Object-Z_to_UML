__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


import xml.dom.minidom
import logging
import xml.sax
from structures import *

logging.getLogger().setLevel(logging.INFO)

dom = xml.dom.minidom.parseString(open('sample.xml').read())

class XMLParser(object):

    def __init__(self, in_file):
        self.generated = []
        dom = xml.dom.minidom.parseString(open(in_file).read())
        self.handleTOZE(dom)

    def getCDATA(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.CDATA_SECTION_NODE:
                rc.append(node.data.strip())
        return ''.join(rc)

    def handleTOZE(self, TOZE):
        self.handleFreeTypeDef(TOZE.getElementsByTagName('freeTypeDef'))
        self.handleBasicTypeDefs(TOZE.getElementsByTagName('basicTypeDef'))
        self.handleClassDef(TOZE.getElementsByTagName('classDef')[0])

    def handleBasicTypeDefs(self, basicTypeDefs):
        for typeDef in basicTypeDefs:
            btd = BasicClass()
            # There may be more than one name there
            # When we figure out how to unescape CDATA, we need to break it down
            # for now, the gnarly string is the name of the object
            btd.name = self.handleStructName(typeDef.getElementsByTagName('name')[0])
            btd.type = 'basicTypeDef'
            logging.info('New basicTypeDef: %s' % btd)
            self.generated.append(btd)

    def handleFreeTypeDef(self, freeTypeDef):
        logging.info("should break here")

    def handleClassDef(self, classDef):
        cls = BasicClass()
        cls.name = self.handleStructName(classDef.getElementsByTagName('name')[0])
        cls.type = 'class'
        # CLASS CHILDREN HANDLERS HERE
        self.generated.append(cls)

    def handleStructName(self, name):
        return self.getCDATA(name.childNodes)
