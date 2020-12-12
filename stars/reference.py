import uuid
from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        reference = None
        if '_reference' in kwargs:
            reference = kwargs['_reference']
        elif len(args) == 1:
            if isinstance(args[0], str):
                if '/' in args[0]:
                    reference = args[0]
                else:
                    reference = args[0] + '/'
            elif isinstance(args[0], Reference):
                reference = args[0]._reference
            elif hasattr(args[0], '__uuid__'):
                reference = args[0].__uuid__
            else:
                raise LookupError('Cannot create reference to "' + str(args[0]) + '"')
        elif len(args) == 2:
            reference = args[0] + '/' + args[1]
        object.__setattr__(self, '_reference', reference)
        object.__setattr__(self, '__cache__', None)

    """ Override the subscript operator """
    def __getitem__(self, name):
        return getattr(self, name)

    """ Override the subscript operator """
    def __setitem__(self, name, value):
        setattr(self, name, value)

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name[0] == '_':
            return object.__getattribute__(self, name)
        elif name == 'is_valid':
            return (self._get(allow_error=False) != None)
        else:
            obj = self._get(create_new=True)
            return obj.__getattribute__(name)

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)
        else:
            obj = self._get(create_new=True)
            if name == 'name':
                object.__setattr__(self, '_reference', obj.__uuid__)
            obj.__setattr__(name, value)

    """ Get/cache the object """
    def _get(self, create_new=False, allow_error=True):
        cache = object.__getattribute__(self, '__cache__')
        if cache == None:
            reference = object.__getattribute__(self, '_reference')
            if reference == None:
                if allow_error:
                    raise LookupError('Uninitialized reference')
            else:
                if create_new and reference.split('/', 1)[1] == '':
                    reference += str(uuid.uuid4())
                    object.__setattr__(self, '_reference', reference)
                cache = game_engine.get(reference, create_new=create_new)
                object.__setattr__(self, '__cache__', cache)
            if cache == None and allow_error:
                raise LookupError('Unable to lookup/create "' + reference + '"')
        return cache

    """ Equality test """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self._reference == other._reference)
