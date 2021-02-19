import json
import uuid
import traceback
from pathlib import Path


""" Base directory for saved games, races, etc """
__game_dir = Path(__file__).parent.parent / 'data'
__user_dir = Path.home() / 'Inherit!'


""" Autosave object """
__auto_save = None


""" Registry of all registered classes and objects """
__registry = []


""" Block registration of new objects """
__registry_block = False


""" Special reference class defined in the reference.py class but needed here for encode/decode indicated by the ® symbol """
_reference_class = None


""" Receive registration of classes and objects as they self-register """
def register(obj):
    global __registry
    global __registry_block
    if not __registry_block:
        __registry.append(obj)


""" Unregister objects to keep them from being part of the save game """
def unregister(obj=None):
    global __auto_save
    global __registry
    if obj:
        __registry.remove(obj)
        if __auto_save == obj:
            __auto_save = None
    else:
        __registry = []
        __auto_save = None


""" Base class for use in creating classes by name """
class BaseClass:
    def __init__(self, **kwargs):
        pass


""" 
Get all registered objects of a type or a specific object
reference is 'Class', 'Class/ID', or 'Class/'+id(obj) 
"""
def get(reference, create_new=False):
    global __registry
    # getting None returns None
    if reference == None:
        return None
    # split reference after forcin string
    ref = str(reference).split('/', 1)
    # get all of a class
    if len(ref) == 1:
        objs = []
        for obj in __registry:
            if obj.__class__.__name__ == ref[0]:
                objs.append(obj)
        return objs
    # find a specific object
    for obj in __registry:
        if obj.__class__.__name__ == ref[0]:
            # match by id
            if str(id(obj)) == ref[1]:
                return obj
            # match by name
            elif getattr(obj, 'ID', '') == ref[1]:
                return obj
    # create and register new object
    if create_new:
        obj = __new(ref[0], None, ID=ref[1])
        return obj
    return None


""" Auto save """
def auto_save():
    global __auto_save
    if __auto_save:
        __auto_save.save()


""" Set auto save object """
def set_auto_save(obj):
    global __auto_save
    __auto_save = obj


""" Decode a string into an object """
def from_json(raw, name='<Internal>'):
    try:
        return __decode(json.loads(raw))
    except Exception as e:
        print('Decode error ' + str(e) + ' in ' + name)


""" Encode an object into a string """
def to_json(obj):
    return json.dumps(__encode(obj), indent='    ', ensure_ascii=False)


""" List files in the game dir """
def load_list(save_type):
    files = []
    dir_name = __game_dir / save_type
    if dir_name.exists():
        for f in dir_name.iterdir():
            files.append(f.name)
    dir_name = __user_dir / save_type
    if dir_name.exists():
        for f in dir_name.iterdir():
            files.append(f.name)
    files.sort()
    return files


""" Load from file, prevent object self registration """
def load_inspect(save_type, name):
    global __registry_block 
    __registry_block = True
    objs = load(save_type, name)
    __registry_block = False
    return objs


""" Load from file, object self registration is assumed """
def load(save_type, name):
    objs = []
    file_name = __user_dir / save_type / name
    if not file_name.exists():
        file_name = __game_dir / save_type / name
    if file_name.is_dir():
        for fname in file_name.iterdir():
            with open(fname, 'r') as f:
                objs.append(from_json(f.read(), str(fname)))
    else:
        with open(file_name, 'r') as f:
            objs.append(from_json(f.read(), str(file_name)))
    if len(objs) == 0:
        return None
    elif len(objs) == 1:
        return objs[0]
    else:
        return objs


""" Save object to file """
def save(save_type, name, obj):
    dir_name = __user_dir / save_type
    dir_name.mkdir(parents=True, exist_ok=True)
    file_name = dir_name / name
    with open(file_name, 'w') as f:
        f.write(to_json(obj))


""" Custom encoder to handle classes """
def __encode(o):
    # Instances of Reference
    if isinstance(o, _reference_class):
        return '«' + o.__reference__ + '»'
    # Handle children of BaseClass and Defaults
    elif isinstance(o, BaseClass):
        encoded = {}
        defaults = getattr(o.__class__, 'defaults', {})
        sparse = getattr(o.__class__, 'sparse_json', {})
        for (k, v) in o.__dict__.items():
            if not sparse.get(k, True):
                encoded[k] = v
            elif k in defaults:
                if v != defaults[k]:
                    encoded[k] = v
            elif k != '__cache__':
                encoded[k] = v
        # Add class
        encoded['__class__'] = o.__class__.__name__
        return __encode(encoded)
    # Encode each key and value
    elif isinstance(o, dict):
        encoded = {}
        for (k, v) in o.items():
            encoded[__encode(k)] = __encode(v)
        return encoded
    # Encode each value
    elif isinstance(o, list) or isinstance(o, tuple):
        encoded = []
        for v in o:
            encoded.append(__encode(v))
        return encoded
    # Finally down to a primitive
    else:
        return o


""" Custom decoder to handle classes """
def __decode(o):
    # Decode each key and value, could be a class
    if isinstance(o, dict):
        decoded = {}
        for (k, v) in o.items():
            decoded[__decode(k)] = __decode(v)
        # It's a class
        if '__class__' in o:
            del decoded['__class__']
            return __new(o['__class__'], decoded, **decoded)
        else:
            return decoded
    # Decode each value
    elif isinstance(o, list) or isinstance(o, tuple):
        decoded = []
        for v in o:
            decoded.append(__decode(v))
        return decoded
    # Could be a reference
    elif isinstance(o, str) and len(o) > 2:
        if o[0] == '«' and o[-1] == '»':
            return _reference_class(o[1:-1])
    # Just a primitive
    return o


""" Find child of BaseClass """
def __new(classname, not_found, **kwargs):
    subclasses = set()
    stack = [BaseClass]
    while stack:
        parent = stack.pop()
        for child in parent.__subclasses__():
            if child.__name__ == classname:
                try:
                    return child(**kwargs)
                except Exception as e:
                    print('Error creating class "' + classname + '"', e)
                    raise e
            elif child not in subclasses:
                subclasses.add(child)
                stack.append(child)
    return not_found
