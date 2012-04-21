__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from xml_parser import XMLParser
from uml_builder import UMLBuilder

parser = XMLParser('sample.xml')
builder = UMLBuilder(parser.classes_list, parser.relations_list, parser.types_list)
builder.gen_uml('uml.uxf')
print parser.classes_list
print parser.relations_list
print parser.types_list