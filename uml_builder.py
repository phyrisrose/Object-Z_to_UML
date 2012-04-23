__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import xml.etree.ElementTree as ET
from xml.dom import minidom

#TODO create relations
#TODO create basic UML object types e.g. BLOCK, USER, etc.

class UMLBuilder(object):

    def __init__(self, classes_list, relations_list, types_list):
        self.classes_list = classes_list
        self.relations_list = relations_list
        self.types_list = types_list

    def gen_uml(self, outfile):
        self.class_x = 20
        self.diagram = ET.Element("diagram", program="umlet", version="11.4")
        self.process_classes()
        self.process_types()
        self.process_relations()

        print ET.tostring(self.diagram)
        #diagram.write(outfile, True)
        #tree_string = self.prettify(ET.tostring(self.diagram, 'utf-8'),outfile)
        tree_string = ET.tostring(self.diagram, 'utf-8')
        f = open(outfile, 'w')
        f.write(tree_string)

    def process_relations(self):
        for rel_el in self.relations_list:
            self.gen_relation(rel_el)

    def process_types(self):
        width = 140
        height = 50
        y_coord = 470
        x_coord = 20
        for type_el in self.types_list:
            self.gen_type(type_el, x_coord, y_coord, width, height)
            x_coord += 160

    #Iterate through all classes, and build uxf elements with gen_class()
    def process_classes(self):
        width = 250
        height = 300
        y_coord = 20
        x_coord = 20
        for type_el in self.classes_list:
            self.gen_class(type_el, x_coord, y_coord, width, height)
            x_coord += 270

    #Build uxf element for classes and type objects
    def gen_class(self, cur_class, x_coord, y_coord, width, height):
        #Create Class
        uxf_class = ET.SubElement(self.diagram, "element")
        uxf_type = ET.SubElement(uxf_class, "type")
        uxf_type.text = "com.umlet.element.Class"
        #Position Class
        uxf_coord = ET.SubElement(uxf_class, "coordinates")
        uxf_coord_x = ET.SubElement(uxf_coord, "x")
        uxf_coord_x.text = str(x_coord)
        uxf_coord_y = ET.SubElement(uxf_coord, "y")
        uxf_coord_y.text = str(y_coord)
        uxf_size_w = ET.SubElement(uxf_coord, "w")
        uxf_size_w.text = str(width)
        uxf_size_h = ET.SubElement(uxf_coord, 'h')
        uxf_size_h.text = str(height)
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

    def gen_type(self, cur_type, x_coord, y_coord, width, height):
        #Create Class
        uxf_class = ET.SubElement(self.diagram, "element")
        uxf_type = ET.SubElement(uxf_class, "type")
        uxf_type.text = "com.umlet.element.Class"
        #Position Class
        uxf_coord = ET.SubElement(uxf_class, "coordinates")
        uxf_coord_x = ET.SubElement(uxf_coord, "x")
        uxf_coord_x.text = str(x_coord)
        uxf_coord_y = ET.SubElement(uxf_coord, "y")
        uxf_coord_y.text = str(y_coord)
        uxf_size_w = ET.SubElement(uxf_coord, "w")
        uxf_size_w.text = str(width)
        uxf_size_h = ET.SubElement(uxf_coord, 'h')
        uxf_size_h.text = str(height)
        #Add Class Contents
        uxf_attributes = ET.SubElement(uxf_class, "panel_attributes")
        class_contents = cur_type.name
        if cur_type.expression != '':
            class_contents += '\n--\n' + cur_type.expression
        if cur_type.predicate != '':
            class_contents += '\n--\n= ' + cur_type.predicate
        uxf_attributes.text = class_contents
        uxf_additional_attributes = ET.SubElement(uxf_class, "additional_attributes")

    def gen_relation(self, relation):
        start_x = 0
        start_y = 0
        end_x = 0
        end_y = 0
        type = relation.type;

        for cla in self.classes_list:
            if cla.name.strip() == relation.start_object:
                relation.start_object = cla
            elif cla.name.strip() == relation.end_object:
                relation.end_object = cla
        for cla in self.types_list:
            if cla.name.strip() == relation.start_object:
                relation.start_object = cla
            elif cla.name.strip() == relation.end_object:
                relation.end_object = cla

        if relation.start_object in self.classes_list:
            start_x = 145 + self.classes_list.index(relation.start_object) * 270
            start_y = 320
        elif relation.start_object in self.types_list:
            start_x = 90 + self.types_list.index(relation.start_object) * 160
            start_y = 470

        if relation.end_object in self.classes_list:
            end_x = 145 + self.classes_list.index(relation.end_object) * 270
            end_y = 320
        elif relation.end_object in self.types_list:
            end_x = 90 + self.types_list.index(relation.end_object) * 160
            end_y = 470

        if start_x < end_x:
            relation_x = start_x - 30
            width = end_x - start_x + 60
        else:
            relation_x = end_x - 30
            width = start_x - end_x + 60

        if start_y < end_y:
            relation_y = start_y - 30
            height = end_y - start_y + 50
        else:
            relation_y = end_y - 30
            height = start_y - end_y + 50

        #Create Relation
        uxf_class = ET.SubElement(self.diagram, "element")
        uxf_type = ET.SubElement(uxf_class, "type")
        uxf_type.text = "com.umlet.element.Relation"
        #Position relation
        uxf_coord = ET.SubElement(uxf_class, "coordinates")
        uxf_coord_x = ET.SubElement(uxf_coord, "x")
        uxf_coord_x.text = str(relation_x)
        uxf_coord_y = ET.SubElement(uxf_coord, "y")
        uxf_coord_y.text = str(relation_y)
        uxf_size_w = ET.SubElement(uxf_coord, "w")
        uxf_size_w.text = str(width)
        uxf_size_h = ET.SubElement(uxf_coord, 'h')
        uxf_size_h.text = str(height)
        #Set type of arrow
        uxf_attributes = ET.SubElement(uxf_class, "panel_attributes")
        if type == 'set_of':
            uxf_attributes.text = "lt=>-"
        elif type == 'comp':
            uxf_attributes.text = "lt=<<<<-\nm1=1\nm2=0..n"
        else:
            uxf_attributes.text = "lt=-"

        uxf_additional_attributes = ET.SubElement(uxf_class, "additional_attributes")
        if end_x > start_x:
            uxf_additional_attributes.text = str(start_x - relation_x) + ';' + \
                                        str(start_y - relation_y) + ';' + \
                                         str(width-20) + ';' + \
                                         str(end_y - relation_y)
        elif start_x > end_x:
                uxf_additional_attributes.text = str(width-20) + ';' +\
                                                 str(start_y - relation_y) + ';' +\
                                                 str(end_x - relation_x) + ';' +\
                                                 str(end_y - relation_y)

    #Make XML pretty
    def prettify(self, txt, outfile):
        cleaned = minidom.parseString(txt)
        return cleaned.toprettyxml(indent = "    ")