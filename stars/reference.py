import uuid
from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        reference = ''
        cache = None
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
                cache = args[0]
            else:
                raise LookupError('Cannot create reference to "' + str(args[0]) + '"')
        elif len(args) == 2:
            reference = args[0] + '/' + args[1]
        object.__setattr__(self, '__reference__', reference)
        object.__setattr__(self, '__cache__', cache)
        if -self == '0c3e2e62-9e82-4e81-8a12-781b39a5d255':
            print('Reference:', game_engine.get(reference, create_new=False))

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
        obj = object.__getattribute__(self, '__get_obj__')(name)
        return obj.__getattribute__(name)

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        obj = object.__getattribute__(self, '__get_obj__')(name)
        obj.__setattr__(name, value)

    """ Dereference the object """
    def __invert__(self):
        return object.__getattribute__(self, '__get_obj__')('~')

    """ Return the class type """
    def __pos__(self):
        return object.__getattribute__(self, '__reference__').split('/', 1)[0]

    """ Return the object ID """
    def __neg__(self):
        return object.__getattribute__(self, '__reference__').split('/', 1)[1]

    """ Get/cache the object """
    def __get_obj__(self, name):
        cache = object.__getattribute__(self, '__cache__')
        if cache == None:
            reference = object.__getattribute__(self, '__reference__')
            if reference == '':
                raise LookupError('Attempting access of "' + name + '" of uninitialized reference')
            else:
                if reference.split('/', 1)[1] == '':
                    reference += str(uuid.uuid4())
                    object.__setattr__(self, '__reference__', reference)
                cache = game_engine.get(reference, create_new=True)
                object.__setattr__(self, '__cache__', cache)
            if cache == None:
                raise LookupError('Attempting access of "' + name + '" but unable to lookup/create "' + reference + '"')
        return cache

    """ Validity test """
    def __bool__(self):
        if object.__getattribute__(self, '__cache__') == None:
            reference = object.__getattribute__(self, '__reference__')
            if reference == '':
                return False
            else:
                if reference.split('/', 1)[1] == '':
                    return False
                cache = game_engine.get(reference, create_new=False)
                object.__setattr__(self, '__cache__', cache)
            if cache == None:
                return False
        return True

    """ Equality test """
    def __eq__(self, other):
        reference = object.__getattribute__(self, '__reference__')
        # Test against a non-reference object
        if type(self) != type(other):
            if hasattr(other, 'ID'):
                return (reference == other.__class__.__name__ + '/' + other.ID)
            return False
        # Test reference, references with just class (no ID) cannot be equal
        return (reference == object.__getattribute__(other, '__reference__') and reference.split('/', 1)[1] != '')
    
    """ Test just the class portion """
    def __xor__(self, classname):
        return (object.__getattribute__(self, '__reference__').split('/', 1)[0] == classname)

    """ Use the reference as the hash """
    def __hash__(self):
        return hash(self.__reference__)

game_engine._reference_class = Reference
Reference.tmp_fields = {'__cache__': True}
