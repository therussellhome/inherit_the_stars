import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'source': [''],
    'icon': [' '],
    'date': [0, 0, sys.maxsize],
    'subject': [''],
    'body': [''],
    'link': [''],
    'unread': [True],
}


""" Message from game, minister, or other player """
class Message(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Message.set_defaults(Message, __defaults)
