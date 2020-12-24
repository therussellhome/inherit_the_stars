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
    """ Get a uid """
    def __init__(self, **kwargs):
        if '__uuid__' in kwargs and '/' in kwargs['__uuid__']:
            self.__uuid__ = kwargs['__uuid__']
        else:
            self.__uuid__ = self.__class__.__name__ + '/' + str(uuid.uuid4())

""" 
Get all registered objects of a type or a specific object
reference is 'Class', 'Class/uid', 'Class/id', or 'Class/Name' 
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
        # match by uid
        if getattr(obj, '__uuid__', '') == reference:
            return obj
        elif obj.__class__.__name__ == ref[0]:
            # match by id
            if str(id(obj)) == ref[1]:
                return obj
            # match by name
            elif getattr(obj, 'name', '') == ref[1]:
                return obj
    # create and register new object
    if create_new:
        obj = __new(ref[0], None, name=ref[1])
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
def __encode(obj):
    values = obj.__dict__.copy()
    cls = obj.__class__
    # special handling for children of Defaults
    defaults = getattr(cls, 'defaults', {})
    for (name, sparse) in getattr(cls, 'sparse_json', {}).items():
        if sparse and name in values and defaults[name][0] == values[name]:
            del values[name]
    if '__uuid__' not in values:
        values['__uuid__'] = cls.__name__ + '/' + str(uuid.uuid4())
    if '__cache__' in values:
        del values['__cache__']
    return values


""" Custom decoder to handle classes """
def __decode(values):
    if '__uuid__' in values:
        classname = values['__uuid__'].split('/')[0]
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
