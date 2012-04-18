__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from uml_builder import UMLBuilder

classes_list = []
relations_list = []
types_list = []
outfile = "uml.xmi"
generator = UMLBuilder(classes_list, relations_list, types_list)
generator.gen_uml(outfile)