__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import xml.etree.ElementTree as ET
from xml.dom import minidom

class UMLBuilder(object):

    def __init__(self, classes_list, relations_list, types_list):
        self.classes_list = classes_list
        self.relations_list = relations_list
        self.types_list = types_list

    def gen_uml(self, outfile):
        self.class_x = 20
        self.diagram = ET.Element("diagram", program="umlet", version="11.4")
        self.process_classes()

        print ET.tostring(self.diagram)
        #diagram.write(outfile, True)
        #tree_string = self.prettify(ET.tostring(self.diagram, 'utf-8'),outfile)
        tree_string = ET.tostring(self.diagram, 'utf-8')
        f = open(outfile, 'w')
        f.write(tree_string)

    #Iterate through all classes, and build uxf elements with gen_class()
    def process_classes(self):
        for class_el in self.classes_list:
            self.gen_class(class_el)

    #Build uxf element for a class
    def gen_class(self, cur_class):
        #Create Class
        uxf_class = ET.SubElement(self.diagram, "element")
        uxf_type = ET.SubElement(uxf_class, "type")
        uxf_type.text = "com.umlet.element.Class"
        #Position Class
        uxf_coord = ET.SubElement(uxf_class, "coordinates")
        uxf_coord_x = ET.SubElement(uxf_coord, "x")
        uxf_coord_x.text = str(self.class_x)
        self.class_x += 270
        uxf_coord_y = ET.SubElement(uxf_coord, "y")
        uxf_coord_y.text = '20'
        uxf_size_w = ET.SubElement(uxf_coord, "w")
        uxf_size_w.text = '250'
        uxf_size_h = ET.SubElement(uxf_coord, 'h')
        uxf_size_h.text = '300'
        #Add Class Contents
        uxf_attributes = ET.SubElement(uxf_class, "panel_attributes")
        class_contents = cur_class.name
        class_contents += '\n--\n'
        #Add Attributes
        if cur_class.attributes != '':
            temp = cur_class.attributes.replace(', ','\n-')
            class_contents += '-' + temp + '\n--\n'
        #Add Operations
        if len(cur_class.functions) > 0:
            for operation in cur_class.functions:

                class_contents += '#' + operation.name + '(' + str(operation.parameter_list) + ')' + '\n'
        uxf_attributes.text = class_contents
        uxf_additional_attributes = ET.SubElement(uxf_class, "additional_attributes")

    #Make XML pretty
    def prettify(self, txt, outfile):
        cleaned = minidom.parseString(txt)
        return cleaned.toprettyxml(indent = "    ")

