from xml.dom import minidom

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import elementtree.ElementTree as ET
import xml.dom.minidom

class UMLBuilder(object):

    def __init__(self, classes_list, relations_list, types_list):
        self.classes_list = classes_list
        self.relations_list = relations_list
        self.types_list = types_list


    def gen_uml(self, outfile):
        xml = ET.Element("?xml version = '1.0' encoding = 'UTF-8' ?")
        xmi = ET.SubElement(xml, "XMI")
        header = ET.SubElement(xmi, "XMI.header")

        content = ET.SubElement(xmi, "XMI.content")
        uml = ET.SubElement(content, "UML:Model")


        self.pretty_print(ET.tostring(xml),outfile)

    def pretty_print(self, txt, outfile):
        print txt
        f = open(outfile, "w")
        f.write(minidom.parseString(txt).toxml())


