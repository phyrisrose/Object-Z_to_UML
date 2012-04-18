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

    def asciiConv(self, name):
        asc_name = list(name)
        ascii = ""
        type_name = ""
        for char in asc_name:
            if char != "&" and char != "#":
                ascii = ascii + char
            if char == '&' and ascii != "":
                type_name += chr(int(ascii))
                new_char = ""
                ascii = ""
        type_name += chr(int(ascii))
        return type_name

    def getCDATA(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.CDATA_SECTION_NODE:
                rc.append(node.data.strip())
        return self.asciiConv(''.join(rc))

    def handleTOZE(self, TOZE):
        if TOZE:
            self.handleFreeTypeDef(TOZE.getElementsByTagName('freeTypeDef'))
            self.handleBasicTypeDefs(TOZE.getElementsByTagName('basicTypeDef'))
            self.handleClassDefs(TOZE.getElementsByTagName('classDef'))
        else:
            logging.info('Finished parsing!')

    #### TOZE Field Handler Methods ####
    #Generic TOZE Fields
    def handleName(self, name):
        return self.getCDATA(name.childNodes)

    def handleStatePredicate(self, predicate):
        # Don't care
        pass

    def handleOperationPredicate(self, predicate):
        # Don't care
        pass

    # Definitions
    def handleAbbreviationDefs(self, abbreviationDefs):
        pass
    def handleAxiomaticDefs(self, axiomaticDefs):
        pass
    def handleBasicTypeDefs(self, basicTypeDefs):
        if basicTypeDefs:
            for typeDef in basicTypeDefs:
                self.handleBasicTypeDef(typeDef)
        else:
            return

    def handleBasicTypeDef(self, basicTypeDef):
        # There may be more than one name there
        # When we figure out how to unescape CDATA, we need to break it down
        # for now, the gnarly string is the name of the object
        names = self.handleName(basicTypeDef.getElementsByTagName('name')[0])
        names = names.split(',')
        for name in names:
            name.strip()
            btd = BasicClass()
            btd.name = name
            btd.type = 'basicTypeDef'
            logging.info('New %s' % btd)
            self.generated.append(btd)

    # TODO: Figure out how to ignore tags that aren't used in the file being parsed.
    def handleFreeTypeDef(self, freeTypeDefs):
        if freeTypeDefs:
            for freeType in freeTypeDefs:
                # do stuff
                pass
        else:
            return

    def handleGenericTypeDefs(self, genericTypeDefs):
        pass

    def handleSchemaDef(self, schemaDefs):
        pass

    #Class specific handlers.
    def handleClassDefs(self, classDefs):
        if classDefs:
            for classDef in classDefs:
                self.handleClassDef(classDef)
        else:
            return

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

    def handleVisibilityLists(self, visibilityLists):
        pass

    def handleInheritedClasses(self, inheritedClasses):
        pass

    def handleState(self, states):
        for state in states:
            self.handleStateDeclaration(state.getElementsByTagName('declaration')[0])
            self.handleStatePredicate(state.getElementsByTagName('predicate')[0])

    # From what I gather, state and operation declarations and predicates
    # serve different purposes. So we need a special one for each
    def handleStateDeclaration(self, declaration):
        if declaration:
            state = self.getCDATA(declaration.childNodes)
            # TODO here we need to put some sort of parser for raw text
            print state
        else:
            return

    def handleInitState(self, initialState):
        pass

    # Operation Handlers
    # it's likely that a class will have several operations,
    # so we have a dedicated function to iterate through all.
    def handleOperations(self, operations):
        if operations:
            functions = []
            for operation in operations:
                functions.append(self.handleOperation(operation))
            return functions
        else:
            return

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
        if declaration:
            state = self.getCDATA(declaration.childNodes)
            # TODO here we need to put some sort of parser for raw text
            print "State! %s" % state
        else:
            return

    def handleOperationDeclaration(self, declaration):
        if declaration:
            dec = self.getCDATA(declaration.childNodes)
            print "Declaration! %s" % dec

    def handleOpDeltaList(self, deltaList):
        if deltaList:
            dl = self.getCDATA(deltaList.childNodes)
            print "return! %s" % dl
            # Uhh... that's just a name, TODO: we need to look up the type of it.
            # Also, what if there are more than one attributes altered?
            # What's going to be the return type?
        pass

    def handleOperationExpression(self, operationExpressions):
        pass
