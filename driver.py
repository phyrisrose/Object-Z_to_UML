__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import sys
from xml_parser import XMLParser
from uml_builder import UMLBuilder

input_file = sys.argv[1]
parser = XMLParser(input_file)
builder = UMLBuilder(parser.classes_list, parser.relations_list, parser.types_list)
print "##########"
print "Lists:"
print "Classes found: %s" % parser.classes_list
print "Relations found: %s" % parser.relations_list
print "Types found: %s" % parser.types_list
print "##########"
builder.gen_uml('uml.uxf')
