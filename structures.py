__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


class BasicClass(object):

    def __init__(self):
        self.name = ''
        self.type = ''
        self.attributes = []  # List of type Object here
        self.functions = []  # List of type Function here

    def __repr__(self):
        return "%s named %s" % (self.type, self.name)


class Function(object):

    def __init__(self):
        self.name = ''
        self.return_type = ''
        self.parameter_list = [] # List of type Object here


#class Inheritance(object):
#
#    def __init__(self):
#        self.parent = ''
#        self.child = ''


class Relation(object):

    def __init__(self):
        self.type = ''
        self.endpoints_a = None
        self.endpoints_b = None
        self.decoration_a = None
        self.decoration_b = None

class TypeDef(object):

    def __init__(self):
        self.name = ''