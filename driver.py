__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from xml_parser import XMLParser
from uml_builder import UMLBuilder

parser = XMLParser('Sam\'s Q3.toze')
builder = UMLBuilder(parser.classes_list, parser.relations_list, parser.types_list)
print "##########"
print "Lists:"
print parser.classes_list
print parser.relations_list
print parser.types_list
print "##########"
builder.gen_uml('uml.uxf')
