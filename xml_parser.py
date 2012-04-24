from xml.dom.expatbuilder import TEXT_NODE
from extended_ascii_lookup import lookup

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

#TODO Handle upper ASCII characters
#TODO Create relations

import xml.dom.minidom
import logging
import re
from structures import *

logging.getLogger().setLevel(logging.INFO)

dom = xml.dom.minidom.parseString(open('sample.xml').read())

class XMLParser(object):

    def __init__(self, in_file):
        self.classes_list = []
        self.relations_list = []
        self.types_list = []
        self.current_class_name = ''
        self.psetExists = False

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
                #Upper ascii isn't handled yet, ignore for now.
                if int(ascii) < 128:
                    type_name += chr(int(ascii))
                else:
                    logging.debug('Ascii in: %s' % int(ascii))
                    type_name += self.handle_upper_ascii(int(ascii))
                ascii = ""
        #Upper ascii isn't handled yet, ignore for now.
        if int(ascii) < 128:
            type_name += chr(int(ascii))
        else:
            type_name += self.handle_upper_ascii(int(ascii))
        return type_name

    def handle_upper_ascii(self, code):
        meaning = lookup.get(code, None)
        if meaning:
            if meaning == "%power_set%":
                self.psetExists = True
            return meaning
        else:
            logging.error('The Special Character Code is Not Valid')


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
                    self.handle_basic_type(node)
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
        for node in node.childNodes:
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
            elif sub_node.nodeName == 'declaration':
                uml_type_obj.name = self.handle_declaration(sub_node)
            elif sub_node.nodeName == 'predicate':
                uml_type_obj.predicate = self.handle_cdata_tag(sub_node)
        self.types_list.append(uml_type_obj)

    def handle_basic_type(self, type_def):
        name_list = []
        for sub_node in type_def.childNodes:
            if sub_node.nodeName == 'name':
                name_list = self.handle_cdata_tag(sub_node).split(',')
        for name in name_list:
            uml_type_obj = TypeDef()
            uml_type_obj.name = name
            self.types_list.append(uml_type_obj)

    def handle_type_in_class(self, type_def, owner_class):
        uml_type_obj = TypeDef()
        for sub_node in type_def.childNodes:
            if sub_node.nodeName == 'name':
                uml_type_obj.name = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'expression':
                uml_type_obj.expression = self.handle_cdata_tag(sub_node)
            elif sub_node.nodeName == 'declaration':
                uml_type_obj.name = self.handle_declaration(sub_node)
        owner_class.internal_type_defs.append(uml_type_obj)

    def handle_schema_def(self, schema_def):
        pass

    #Class specific handlers.
    def handle_class_def(self, class_def):
        uml_class_obj = BasicClass()
        for sub_node in class_def.childNodes:
            if sub_node.nodeName == 'name':
                uml_class_obj.name = self.handle_cdata_tag(sub_node)
                self.current_class_name = uml_class_obj.name
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
        uml_class_obj.type = 'Class'
        self.classes_list.append(uml_class_obj)

    def handle_state(self, state_node, parent_uml_obj):
        for sub_node in state_node.childNodes:
            if sub_node.nodeName == 'name':
                parent_uml_obj.attributes += '\n?' + self.handle_cdata_tag(sub_node) + '?\n'
            elif sub_node.nodeName == 'declaration':
                declaration = self.handle_declaration(sub_node)
                self.relation_builder(declaration)
                parent_uml_obj.attributes += declaration
            elif sub_node.nodeName == 'predicate':
                parent_uml_obj.predicate_rules += self.handle_cdata_tag(sub_node)

    def handle_operation(self, node, parent_uml_obj):
        uml_func_obj = Function()
        for sub_node in node.childNodes:
            if sub_node.nodeName == 'name':
                uml_func_obj.name = self.handle_cdata_tag(sub_node)
            #elif sub_node.nodeName == 'deltaList':
            #    uml_func_obj.parameter_list = self.handle_parameter_list(sub_node)
            elif sub_node.nodeName == 'declaration':
                uml_func_obj.parameter_list = self.handle_declaration(sub_node)
            elif sub_node.nodeName == 'predicate':
                uml_func_obj.predicate = self.handle_cdata_tag(sub_node)
        parent_uml_obj.functions.append(uml_func_obj)

    def handle_declaration(self, node):
        cdata = self.handle_cdata_tag(node)
        params = ''
        for char in list(cdata):
            if char == '\n':
                params += ', '
            elif char != '?':
                params += char
        return params

    def handle_bare_predicate(self, node):
        pass

    def relation_builder(self, declaration):
        """
        Take data from a declaration tag that has been translated from ASCII
        and reformatted by 'handle_declaration()' function and search for relations
        """
        attr_template = r'\w*: *(\w*) *(%.*%) *(\w*)'
        pattern = re.compile(attr_template)
        declaration_lines = declaration.split(', ')
        for line in declaration_lines:
            match = pattern.match(line)
            if match:
                if 'relation' in match.group(2):
                    rel = Relation()
                    rel.start_object = match.group(1)
                    if 'int' in match.group(3):
                        rel.end_object = "Integers"
                        zExists = False
                        for type in self.types_list:
                            if type.name == "Integers":
                                zExists = True
                        if not zExists:
                            intType = TypeDef()
                            intType.name = "Integers"
                            self.types_list.append(intType)
                    elif 'natural' in match.group(3):
                        rel.end_object = "Natural Numbers\n(N)"
                        zExists = False
                        for type in self.types_list:
                            if type.name == "Natural Numbers\n(N)":
                                zExists = True
                        if not zExists:
                            intType = TypeDef()
                            intType.name = "Natural Numbers\n(N)"
                            self.types_list.append(intType)
                    elif 'real' in match.group(3):
                        rel.end_object = "Real Numbers\n(N)"
                        zExists = False
                        for type in self.types_list:
                            if type.name == "Real Numbers\n(N)":
                                zExists = True
                        if not zExists:
                            intType = TypeDef()
                            intType.name = "Real Numbers\n(N)"
                            self.types_list.append(intType)
                    else:
                        rel.end_object = match.group(3)
                    rel.type = ((match.group(2)).strip('%')).strip('_relation')
                    self.relations_list.append(rel)
                if 'power_set' in match.group(2):
                    set_rel = Relation()
                    set_rel.type = "comp"
                    set_rel.start_object = self.current_class_name
                    set_rel.end_object = match.group(3)
                    self.relations_list.append(set_rel)
