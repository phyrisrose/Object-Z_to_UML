__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

#TODO figure out what to do if the major elements are not defined in predicted order.
# for example, basicTypeDef came after classDef

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
            btd.name = self.handleName(typeDef.getElementsByTagName('name')[0])
            btd.type = 'basicTypeDef'
            logging.info('New %s' % btd)
            self.generated.append(btd)

    # TODO: Figure out how to ignore tags that aren't used in the file being parsed.
    def handleFreeTypeDef(self, freeTypeDef):
        logging.info("should break here, freeTypeDef is undefined in the current doc")

    def handleClassDef(self, classDef):
        cls = BasicClass()
        cls.name = self.handleName(classDef.getElementsByTagName('name')[0])
        cls.type = 'class'
        # CLASS CHILDREN HANDLERS HERE
        self.handleState(classDef.getElementsByTagName('state'))
        self.handleInitState(classDef.getElementsByTagName('initialState')[0])
        ftns_to_append = self.handleOperations(classDef.getElementsByTagName('operation'))
        cls.functions.append(ftns_to_append)
        # by this point, the class entity should be complete
        logging.info("New %s" % cls)
        self.generated.append(cls)

    def handleName(self, name):
        return self.getCDATA(name.childNodes)

    def handleState(self, states):
        for state in states:
            # do something with state
            self.handleStateDeclaration(state.getElementsByTagName('declaration')[0])
            self.handleStatePredicate(state.getElementsByTagName('predicate')[0])

    def handleInitState(self, initialState):
        pass

    # it's likely that a class will have several operations,
    # so we have a dedicated function to iterate through all.
    def handleOperations(self, operations):
        functions = []
        for operation in operations:
            functions.append(self.handleOperation(operation))
        return functions

    def handleOperation(self, operation):
        ftn = Function()
        ftn.name = self.handleName(operation.getElementsByTagName('name')[0])
        self.handleOpDeltaList(operation.getElementsByTagName('deltaList')[0])
        self.handleOperationDeclaration(operation.getElementsByTagName('declaration')[0])
        self.handleOperationPredicate(operation.getElementsByTagName('predicate')[0])
        # assume the previous functions gathered some data, now we
        # ftn.append_some_attributes_to_the_object
        # and pass it up to handleOperations()
        logging.info('New Function %s' % ftn.name)
        return ftn

    # From what I gather, state and operation declarations and predicates
    # serve different purposes. So we need a special one for each
    def handleStateDeclaration(self, declaration):
        pass

    def handleOperationDeclaration(self, declaration):
        pass

    def handleStatePredicate(self, predicate):
        pass

    def handleOperationPredicate(self, predicate):
        pass

    def handleOpDeltaList(self, deltaList):
        pass
