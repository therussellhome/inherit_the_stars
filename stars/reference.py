import uuid
from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        reference = ''
        if '__reference__' in kwargs:
            reference = kwargs['__reference__']
        elif len(args) == 1:
            if isinstance(args[0], Reference):
                reference = args[0].__reference__
            elif isinstance(args[0], str):
                if '/' in args[0]:
                    reference = args[0]
                else:
                    reference = args[0] + '/'
            elif hasattr(args[0], 'ID'):
                reference = args[0].__class__.__name__ + '/' +  args[0].ID
            else:
                raise LookupError('Cannot create reference to "' + str(args[0]) + '"')
        elif len(args) == 2:
            reference = args[0] + '/' + args[1]
        object.__setattr__(self, '__reference__', reference)
        object.__setattr__(self, '__cache__', None)

    """ Override the subscript operator """
    def __getitem__(self, name):
        return getattr(self, name)

    """ Override the subscript operator """
    def __setitem__(self, name, value):
        setattr(self, name, value)

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name[:2] == '__':
            return object.__getattribute__(self, name)
        obj = object.__getattribute__(self, '__get_obj__')()
        return obj.__getattribute__(name)

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        obj = object.__getattribute__(self, '__get_obj__')()
        obj.__setattr__(name, value)

    """ Get/cache the object """
    def __get_obj__(self):
        cache = object.__getattribute__(self, '__cache__')
        if cache == None:
            reference = object.__getattribute__(self, '__reference__')
            if reference == '':
                raise LookupError('Uninitialized reference')
            else:
                if reference.split('/', 1)[1] == '':
                    reference += str(uuid.uuid4())
                    object.__setattr__(self, '__reference__', reference)
                cache = game_engine.get(reference, create_new=True)
                object.__setattr__(self, '__cache__', cache)
            if cache == None:
                raise LookupError('Unable to lookup/create "' + reference + '"')
        return cache

    """ Equality test """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (object.__getattribute__(self, '__reference__') == object.__getattribute__(other, '__reference__'))

    
    """ Test just the class portion """
    def __xor__(self, classname):
        return (object.__getattribute__(self, '__reference__').split('/', 1)[0] == classname)


    """ Use the reference as the hash """
    def __hash__(self):
        return hash(self.__reference__)

game_engine._reference_class = Reference
