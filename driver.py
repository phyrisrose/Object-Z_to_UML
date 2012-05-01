__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from xml_parser import XMLParser
from uml_builder import UMLBuilder
import sys

if sys.argv:
    parser = XMLParser(sys.argv[1])
    builder = UMLBuilder(parser.classes_list, parser.relations_list, parser.types_list)
    print "##########"
    print "Lists:"
    print "Classes found: %s" % parser.classes_list
    print "Relations found: %s" % parser.relations_list
    print "Types found: %s" % parser.types_list
    print "##########"
    builder.gen_uml('uml.uxf')
else:
    print "No input file specified. Please specify the location of a TOZE Object-Z specification as argument 1."