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
        tree_string = self.prettify(ET.tostring(self.diagram, 'utf-8'),outfile)
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
        self.class_x += 220
        uxf_coord_y = ET.SubElement(uxf_coord, "y")
        uxf_coord_y.text = '20'
        uxf_size_w = ET.SubElement(uxf_coord, "w")
        uxf_size_w.text = '200'
        uxf_size_h = ET.SubElement(uxf_coord, 'h')
        uxf_size_h.text = '300'
        #Add Class Contents
        uxf_attributes = ET.SubElement(uxf_class, "panel_attributes")
        class_contents = cur_class.name
        class_contents += '\n--\n'
        #Add Attributes
        if len(cur_class.attributes) > 0:
            for attribute in cur_class.attributes:
                class_contents += '-' + attribute.name + ': ' + attribute.type + '\n'
            class_contents += '--\n'
        #Add Operations
        if len(cur_class.functions) > 0:
            for operation in cur_class.functions:
                params = ''
                for var in operation.parameter_list:
                    #params += var + ','
                    if len(var) > 1:
                        params += var.name + ':' + var.type + ','
                    else:
                        params += var
                #params = params[:-1] #Strip the last comma from params list
                class_contents += operation.name + '(' + params + ')' + '\n'
        uxf_attributes.text = class_contents
        uxf_additional_attributes = ET.SubElement(uxf_class, "additional_attributes")

    #Make XML pretty
    def prettify(self, txt, outfile):
        cleaned = minidom.parseString(txt)
        return cleaned.toprettyxml(indent = "    ")

