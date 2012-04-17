__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import inspect
import logging
import xml.sax
from structures import *

logging.getLogger().setLevel(logging.INFO)

class XMLParser(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.cur_object = None # To keep track of the current object when we encounter attribute tags
        self.cur_tag = None # To keep track of a cur tag for correlating CDATA
        self.generated = []

    def startElement(self, name, attrs):
        print("startElement: <%s>" % name)
        try:
            getattr(self,'%s' % name)() # This calls a member function to handle that which is in the "name"
        except AttributeError:
            logging.error("Tag undefined <%s>" % name)

    def endElement(self, name):
    #        print("endElement '" + name + "'")
        pass

    def characters(self, content):
        content = content.strip()
        if content:
            content = content.encode('ascii')
            try:
                getattr(self,'%s' % self.cur_tag)(content) # This calls a member function with a CDATA parameter
            except AttributeError:
                logging.error("Tag undefined <%s>" % self.cur_tag)
            print("characters: %s" % content)

    @classmethod
    def whoami(cls):
        return inspect.stack()[1][3]


    ################# Handlers ######################
    # Convention: all handler methods need to have the same name as the name of the
    # tag they are processing. Ew, camel back notation.

    def basicTypeDef(self):
        btd = BasicClass()
        btd.type = XMLParser.whoami() # Set object type, while we are at it
        self.generated.append(btd)
        self.cur_object = btd

    def classDef(self):
        cls = BasicClass()
        cls.type = XMLParser.whoami() # Set object type, while we are at it
        self.generated.append(cls)
        self.cur_object = cls

    def declaration(self):
        pass

    def deltaList(self):
        pass

    def initialState(self):
        pass

    def name(self, cdata=None):
        self.cur_tag = XMLParser().whoami()
        logging.debug("I am %s" % self.cur_tag)
        if cdata:
            self.cur_object.name = cdata
        else:
            self.cur_object.name = 'Touched'

    def operation(self):
        fun = Function()
        self.cur_object.functions.append(fun)

    def predicate(self):
        pass

    def state(self):
        pass



def main():
    source = open('sample.xml')
    parser = XMLParser()
    xml.sax.parse(source, parser)
    print parser.generated

main()