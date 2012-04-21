from xml.dom.expatbuilder import TEXT_NODE

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


import xml.dom.minidom
import logging
from structures import *

logging.getLogger().setLevel(logging.INFO)

dom = xml.dom.minidom.parseString(open('sample.xml').read())

class XMLParser(object):

    def __init__(self, in_file):
        self.classes_list = []
        self.relations_list = []
        self.types_list = []

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
        self.toze_parse(TOZE.firstChild)

    def toze_parse(self, root_node):
        for node in root_node.childNodes:
            if node.nodeType != TEXT_NODE:
                if node.nodeName == 'abbreviationDef':
                    self.handle_type(node)
                elif node.nodeName == 'axiomaticDef':
                    self.handle_type(node)
                elif node.nodeName == 'basicTypeDef':
                    self.handle_type(node)
                elif node.nodeName == 'freeTypeDef':
                    self.handle_type(node)
                elif node.nodeName == 'genericTypeDef':
                    self.handle_type(node)
                elif node.nodeName == 'schemaDef':
                    self.handle_schema_def(node)
                elif node.nodeName == 'classDef':
                    self.handle_class_def(node)
                elif node.nodeName == 'predicate':
                    self.handle_bare_predicate(node)
                else:
                    print"Unparsed node: " + node

    #### TOZE Field Handler Methods ####
    # Definitions

    def handle_cdata_tag(self, node):
        cdata_string = ''
        if node.nodeType == node.CDATA_SECTION_NODE:
            cdata_string = self.asciiConv(node.data.strip())
        return cdata_string
    
    def handle_type(self, type_def):
        uml_type_obj = TypeDef()
        for sub_node in type_def.childNodes:
            if sub_node.nodeName == 'name':
                uml_type_obj.name = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'expression':
                uml_type_obj.expression = self.handle_cdata_tag(sub_node)
        self.types_list.append(uml_type_obj)

    def handle_type_in_class(self, type_def, owner_class):
        uml_type_obj = TypeDef()
        for sub_node in type_def.childNodes:
            if sub_node.nodeName == 'name':
                uml_type_obj.name = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'expression':
                uml_type_obj.expression = self.handle_cdata_tag()
        owner_class.internal_type_defs.append(uml_type_obj)

    def handle_schema_def(self, schema_def):
        pass

    #Class specific handlers.
    def handle_class_def(self, class_def):
        uml_class_obj = BasicClass()
        for sub_node in class_def.childNodes:
            if sub_node.nodeName == 'name':
                uml_class_obj.name = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'visibilityList':
                uml_class_obj.vis_list = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'inheritedClass':
                uml_class_obj.inherited_class = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'abbreviationDef':
                self.handle_type_in_class(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'axiomaticDef':
                self.handle_type_in_class(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'basicTypeDef':
                self.handle_type_in_class(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'freeTypeDef':
                self.handle_type_in_class(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'genericTypeDef':
                self.handle_type_in_class(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'state':
                self.handle_state(sub_node, uml_class_obj)
            elif sub_node.nodeName == 'operation':
                self.handle_operation(sub_node, uml_class_obj)
        self.classes_list.append(uml_class_obj)

    def handle_state(self,sub_node, uml_class_obj):
        pass

    def handle_operation(self, node, parent_uml_obj):
        uml_func_obj = Function()
        for sub_node in node.childNodes:
            if sub_node.nodeName == 'name':
                uml_func_obj.name = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'deltaList':
                uml_func_obj.parameter_list = self.getCDATA(sub_node.childNodes)
            elif sub_node.nodeName == 'declaration':
                uml_func_obj.declaration = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'predicate':
                uml_func_obj.predicate = self.handle_cdata_tag(sub_node)
        parent_uml_obj.functions.append(uml_func_obj)

    def handle_bare_predicate(self, node):
        pass