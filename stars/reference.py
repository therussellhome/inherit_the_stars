from . import game_engine


""" Encapsulate a reference to another class, using game_engine to lookup or create new """
# Inherit from BaseClass so that from_json can create the class
class Reference(game_engine.BaseClass):
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        if '_reference' in kwargs:
            self._reference = kwargs['_reference']
        elif len(args) == 1:
            if isinstance(args[0], str):
                if '/' in args[0]:
                    self._reference = args[0]
                else:
                    self._reference = args[0] + '/'
            elif isinstance(args[0], Reference):
                self._reference = args[0]._reference
            elif not hasattr(args[0], 'name'):
                raise LookupError('Cannot create reference to ' + str(args[0]))
            else:
                self._reference = args[0].__class__.__name__ + '/' + args[0].name
        elif len(args) == 2:
            self._reference = args[0] + '/' + args[1]
        else:
            self._reference = None

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name[0] == '_':
            return object.__getattribute__(self, name)
        else:
            reference = self._reference
            if name == 'is_valid':
                obj = game_engine.get(reference, create_new=False)
                return (obj != None)
            elif reference == None:
                raise LookupError('Uninitialized reference')
            elif name == 'name':
                return reference.split('/', 1)[1]
            if reference.split('/', 1)[1] == '':
                reference += str(id(self))
                self._reference = reference
            obj = game_engine.get(reference, create_new=True)
            if obj != None:
                return obj.__getattribute__(name)
            else:
                raise LookupError('Unable to lookup/create "' + reference + '"')

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)
        else:
            reference = self._reference
            if reference == None:
                raise LookupError('Uninitialized reference')
            elif name == 'name':
                reference = reference.split('/')[0] + '/' + value
                self._reference = reference
            elif reference.split('/', 1)[1] == '':
                reference += str(id(self))
                self._reference = reference
            obj = game_engine.get(reference, create_new=True)
            if obj != None:
                obj.__setattr__(name, value)
            else:
                raise LookupError('Unable to lookup/create "' + reference + '"')

    """ Equality test """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self._reference == other._reference)
