from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        if 'reference' in kwargs:
            self.reference = kwargs['reference']
        elif len(args) > 1:
            self.reference = args[0] + '/' + args[1]
        elif len(args) == 1:
            self.reference = args[0].__class__.__name__ + '/' + args[0].name
        else:
            self.reference = None

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name == 'reference' or name[0] == '_':
            return object.__getattribute__(self, name)
        else:
            reference = object.__getattribute__(self, 'reference')
            obj = game_engine.get(reference)
            if name == 'is_valid':
                return (obj != None)
            elif obj != None:
                return obj.__getattribute__(name)
            else:
                raise LookupError('"' + str(reference) + '" is not registered')

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        if name == 'reference' or name[0] == '_':
            self.__dict__[name] = value
        else:
            reference = object.__getattribute__(self, 'reference')
            obj = game_engine.get(reference)
            if obj != None:
                obj.__setattr__(name, value)
            else:
                raise LookupError('"' + str(reference) + '" is not registered')
