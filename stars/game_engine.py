import json
from pathlib import Path


""" Base directory for saved games, races, etc """
__game_dir = Path.home() / 'Inherit!'
__default_data = Path(__file__).parent.parent / 'default_data'



""" Registry of all registered classes and objects """
__registry = []


""" Block registration of new objects """
__registry_block = False


""" Receive registration of classes and objects as they self-register """
def register(obj):
    global __registry
    global __registry_block
    if not __registry_block:
        __registry.append(obj)
    else:
        print('registration blocked', obj)


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
Get all registered objects of a type or a specific object
objkey can be the objects name attribute or it's id
"""
def get(classname, objkey=None, create_new=False):
    global __registry
    # getting None returns None
    if classname == None:
        return None
    # reference must be a string
    if not isinstance(classname, str):
        classname = str(classname)
    objs = []
    for obj in __registry:
        if obj.__class__.__name__ == classname:
            # match by id
            if str(id(obj)) == objkey:
                return obj
            # match by name
            elif getattr(obj, 'name', '') == objkey:
                return obj
            else:
                objs.append(obj)
    # return by type if no key
    if objkey == None:
        return objs
    # create and register new object
    if create_new:
        obj = __new(classname, None, name=objkey)
        register(obj)
        return obj
    return None


""" Decode a string into an object """
def from_json(raw, name='<Internal>'):
    try:
        return json.loads(raw, object_hook=__decode)
    except Exception as e:
        print('Decode error ' + str(e) + ' in ' + name + '\n' + raw)


""" Encode an object into a string """
def to_json(obj):
    return json.dumps(obj, indent='    ', default=__encode)


""" List files in the game dir """
def load_list(save_type):
    files = []
    dir_name = __game_dir / save_type
    dir_name.mkdir(parents=True, exist_ok=True)
    for f in dir_name.iterdir():
        files.append(f.name)
    files.sort()
    return files


""" Load from file, prevent object self registration """
def load_inspect(save_type, name):
    global __registry_block 
    file_name = __game_dir / save_type / name
    obj = None
    __registry_block = True
    with open(file_name, 'r') as f:
        obj = from_json(f.read(), str(file_name))
    __registry_block = False
    return obj


""" Load from file, object self registration is assumed """
def load(save_type, name):
    file_name = __game_dir / save_type / name
    obj = None
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
