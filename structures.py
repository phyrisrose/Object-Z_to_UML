__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


class BasicClass(object):

    def __init__(self):
        self.name = ''
        self.type = ''
        self.attributes = ''  # List of type Object here
        self.functions = []  # List of type Function here
        self.internal_type_defs = []
        self.vis_list = []
        self.predicate_rules = ''

    def __repr__(self):
        return "%s named %s" % (self.type, self.name)


class Function(object):

    def __init__(self):
        self.name = ''
        self.return_type = ''
        self.parameter_list = '' # List of type Object here
        self.declaration = ''
        self.predicate = ''

    def __repr__(self):
        return "<Function named %s with parameters: %s>" % (self.name,self.parameter_list)


#class Inheritance(object):
#
#    def __init__(self):
#        self.parent = ''
#        self.child = ''


class Relation(object):

    def __init__(self):
        self.type = ''
        self.start_object = None
        self.end_object = None

    def __repr__(self):
        return "<Relation of type %s from %s to %s>" % (self.type,
                                                        self.start_object,
                                                        self.end_object)

class VarDef(object):

    def __init__(self):
        self.name = ''
        self.type = ''
    def __repr__(self):
        return "<VarDef named %s of type %s>" % (self.name,self.type)

class TypeDef(object):

    def __init__(self):
        self.name = ''
        self.type = ''
        self.expression = ''
        self.declaration = ''
        self.predicate = ''
    def __repr__(self):
        return "<TypeDef named %s>" % (self.name)