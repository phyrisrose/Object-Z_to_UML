__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


class BasicClass(object):

    def __init__(self):
        self.instance_var = {} # of the form {name: type}
        self.function = '' # instance of Function class goes here


class Function(object):

    def __init__(self):
        self.name = ''
        self.return_type = ''
        self.parameter = []
        self.parameter_type = []


class Inheritance(object):

    def __init__(self):
        self.parent = ''
        self.child = ''


class Relation(object):

    def __init__(self):
        self.from_c = '' # here goes UML class, figure out later
        self.to_c = ''
