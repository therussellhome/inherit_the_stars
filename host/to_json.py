import json
import os
from zipfile import ZipFile, ZipInfo
from planet import Planet
from serializable import Serializable

""" Custom encoder to handle classes """
def __encode(obj):
    d = obj.__dict__
    d['__class__'] = obj.__class__.__name__
    return d

""" Custom decoder to handle classes """
def __decode(d):
    if '__class__' in d:
        for c in Serializable.__subclasses__():
            if c.__name__ == d['__class__']:
                obj = c()
                obj.__dict__ = d
                return obj
    return d

""" Write a class to file """
def write(filename, obj):
    with open(filename, 'w') as f:
        json.dump(obj, f, default=__encode)

""" Read a class from file """
def read(filename):
    with open(filename) as f:
        return json.load(f, object_hook=__decode)

""" Open zip file """
def load_game(path):
    with ZipFile(path, 'r') as zipfile:
        for info in zipfile.infolist():
            with zipfile.open(info.filename) as f:
                json.load(f, object_hook=__decode)
    pass

""" Update zip file """
def save_game(path):
    p1 = Planet(name='p1')
    p2 = Planet(name='p2')
    with ZipFile(path, 'w') as zipfile:
        zipfile.writestr(ZipInfo('p1.json'), json.dumps(p1, default=__encode))
        zipfile.writestr(ZipInfo('p2.json'), json.dumps(p2, default=__encode))

""" Class used for testing """
class _TestClass(Serializable):
    def __init__(self, name='_TestClass'):
        self.name = name

""" Test method """
def _test():
    print('to_json._test - begin')
    save_game('to_json.zip')
    try:
        os.remove('to_json.test')
    except:
        pass
    write('to_json.test', _TestClass('this is a test'))
    t = read('to_json.test')
    if t.name != 'this is a test':
        print('to_json._test - ERROR: expected "this is a test", got "' + t.name + '"')
    os.remove('to_json.test')
    print('to_json._test - end')
