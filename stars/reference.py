from random import random
from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        self_dict = object.__getattribute__(self, '__dict__')
        self_dict['__class'] = None
        self_dict['__name'] = random()
        if '__class' in kwargs:
            self_dict['__class'] = kwargs['__class']
            if '__name' in kwargs:
                self_dict['__name'] = kwargs['__name']
        elif len(args) > 1:
            self_dict['__class'] = args[0]
            self_dict['__name'] = args[1]
        elif len(args) == 1:
            self_dict['__class'] = args[0].__class__.__name__
            self_dict['__name'] = args[0].name

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name[0] == '_':
            return object.__getattribute__(self, name)
        else:
            self_dict = object.__getattribute__(self, '__dict__')
            reference = None
            if self_dict['__class'] != None:
                reference = self_dict['__class'] + '/' + self_dict['__name']
            obj = game_engine.get(reference, create_new=True)
            if name == 'is_valid':
                return (obj != None)
            elif obj != None:
                return obj.__getattribute__(name)
            elif name == 'name':
                return object.__getattribute__(self, '__name')
            else:
                raise LookupError('"' + str(reference) + '" is not registered')

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        self_dict = object.__getattribute__(self, '__dict__')
        if name[0] == '_':
            self_dict[name] = value
        else:
            reference = self_dict['__class'] + '/' + self_dict['__name']
            obj = game_engine.get(reference, create_new=True)
            if name == 'name':
                self.__dict__['name'] = value
            if obj != None:
                obj.__setattr__(name, value)
            elif name != 'name':
                raise LookupError('"' + str(reference) + '" is not registered')
