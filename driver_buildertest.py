__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from uml_builder import UMLBuilder
import structures

object_a = structures.TypeDef()
object_a.name = 'a'
object_a.type = 'int'

object_b = structures.TypeDef()
object_b.name = 'b'
object_b.type = 'float'

object_c = structures.TypeDef()
object_c.name = 'c'
object_c.type = 'Char'

function_a = structures.Function()
function_a.name = 'foo'
function_a.parameter_list = [object_a, object_b]

function_b = structures.Function()
function_b.name = 'bar'
function_b.parameter_list = [object_b, object_c]

class_a = structures.BasicClass()
class_a.name = 'ClassA'
class_a.type = ''
class_a.attributes = [object_a, object_b, object_c]
class_a.functions = [function_a, function_b]

class_b = structures.BasicClass()
class_b.name = 'ClassB'
class_b.type = ''
class_b.attributes = [object_b, object_c]
class_b.functions = [function_a]

classes_list = [class_a, class_b]
relations_list = []
types_list = []
outfile = "uml.uxf"
generator = UMLBuilder(classes_list, relations_list, types_list)
generator.gen_uml(outfile)