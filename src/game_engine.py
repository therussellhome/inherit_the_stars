import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo


""" Base directory for saved games, races, etc """
__game_dir = Path.home() / 'stars'


""" Registry of all game objects """
__registry = []


""" Receive registration of classes and objects as they self-register """
def register(obj):
    __registry.append(obj)


""" Unregister objects to keep them from being part of the save game """
def unregister(obj):
    if obj:
        __registry.remove(obj)
    else:
        __registry = []


""" Base class for use in creating classes by name """
class BaseClass:
    pass


""" Get a referenced class by name """
def get(reference):
    # get all of a type
    if reference[-1:] == '/':
        objs = []
        for obj in __registry:
            if obj.__class__.__name__ + '/' == reference:
                objs.append(obj)
        return objs
    # get object from registry
    for obj in __registry:
        if hasattr(obj, 'name'):
            if reference == obj.__class__.__name__ + '/' + obj.name:
                return obj
    # create new object
    (classname, obj_name) = reference.split('/')
    return __new(classname, None, name=obj_name)


""" Decode a string into an object """
def from_json(string):
	return json.loads(string, object_hook=__decode)


""" Encode an object into a string """
def to_json(obj):
	return json.dumps(obj, default=__encode)


""" List files in the game dir """
def load_list(save_type):
    files = []
    for f in (__game_dir / save_type).iterdir():
        # strip the .zip
        files.append(f.name[0:-4])
    files.sort()
    return files


""" Load game from zip file """
def load(save_type, name):
    game_file = __game_dir / save_type / (name + '.zip')
    with ZipFile(game_file, 'r') as zipfile:
        for info in zipfile.infolist():
            register(from_json(zipfile.read(info)))


""" Save game to zip file """
def save(save_type, name, objs=__registry):
    game_file = __game_dir / (name + '.zip')
    game_file.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(game_file, 'w') as zipfile:
        for obj in objs:
            name = getattr(obj, 'name', str(id(obj)))
            zipfile.writestr(ZipInfo(name), to_json(obj))


""" Custom encoder to handle classes """
def __encode(obj):
    values = obj.__dict__.copy()
    values['__class__'] = obj.__class__.__name__
    return values


""" Custom decoder to handle classes """
def __decode(values):
    if '__class__' in values:
        return __new(values['__class__'], values, **values)
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