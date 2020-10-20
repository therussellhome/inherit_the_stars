import json
from pathlib import Path


""" Base directory for saved games, races, etc """
__game_dir = Path.home() / 'Inherit!'
__default_data = Path(__file__).parent.parent / 'default_data'



""" Registry of all registered classes and objects """
__registry = []


""" Receive registration of classes and objects as they self-register """
def register(obj):
    global __registry
    __registry.append(obj)


""" Unregister objects to keep them from being part of the save game """
def unregister(obj=None):
    global __registry
    if obj:
        __registry.remove(obj)
    else:
        __registry = []


""" Base class for use in creating classes by name """
class BaseClass:
    pass


""" 
Get a referenced class by name 
reference can be 'Class/ObjName', 'Class/Id', or 'Class'
"""
def get(reference, create_new=False):
    global __registry
    # getting None returns None
    if reference == None:
        return None
    # reference must be a string
    if not isinstance(reference, str):
        reference = str(reference)
    # get all of a type
    if '/' not in reference:
        objs = []
        for obj in __registry:
            if obj.__class__.__name__ == reference:
                objs.append(obj)
        return objs
    # get object from registry
    for obj in __registry:
        if reference == obj.__class__.__name__ + '/' + str(id(obj)):
            return obj
        if hasattr(obj, 'name'):
            if reference == obj.__class__.__name__ + '/' + obj.name:
                return obj
    # create and register new object
    if create_new:
        (classname, obj_name) = reference.split('/')
        obj = __new(classname, None, name=obj_name)
        register(obj)
        return obj
    return None


""" Decode a string into an object """
def from_json(string, name='<Internal>'):
    try:
	    return json.loads(string, object_hook=__decode)
    except Exception as e:
        print('Decode error ' + str(e) + ' in ' + name + '\n' + string)


""" Encode an object into a string """
def to_json(obj):
	return json.dumps(obj, default=__encode)


""" List files in the game dir """
def load_list(save_type):
    files = []
    dir_name = __game_dir / save_type
    dir_name.mkdir(parents=True, exist_ok=True)
    for f in dir_name.iterdir():
        files.append(f.name)
    files.sort()
    return files


""" Load from file, object self registration is assumed """
def load(save_type, name):
    file_name = __game_dir / save_type / name
    with open(file_name, 'r') as f:
        obj = from_json(f.read(), str(file_name))
        return obj


""" Load tech from loose files """
def load_defaults(save_type):
    objs = []
    for file_name in (__default_data / save_type).iterdir():
        with open(file_name, 'r') as f:
            obj = from_json(f.read(), str(file_name))
            objs.append(obj)
    return objs


""" Save object to file """
def save(save_type, name, obj):
    dir_name = __game_dir / save_type
    dir_name.mkdir(parents=True, exist_ok=True)
    file_name = dir_name / name
    with open(file_name, 'w') as f:
        f.write(to_json(obj))


""" Custom encoder to handle classes """
def __encode(obj):
    values = obj.__dict__.copy()
    values['__class__'] = obj.__class__.__name__
    return values


""" Custom decoder to handle classes """
def __decode(values):
    if '__class__' in values:
        classname = values['__class__']
        del values['__class__']
        return __new(classname, values, **values)
    return values


""" Find child of BaseClass """
def __new(classname, not_found, **kwargs):
    subclasses = set()
    stack = [BaseClass]
    while stack:
        parent = stack.pop()
        for child in parent.__subclasses__():
            if child.__name__ == classname:
                return child(**kwargs)
            elif child not in subclasses:
                subclasses.add(child)
                stack.append(child)
    return not_found
