import sys
import time
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'date': [''],
    'timestamp': [0, 0, sys.maxsize],
    'msg_key': [''],
    'parameters': [[]],
    'sender': [''],
    'link': [''],
    'keep': [False],
}


""" Message from game, minister, or other player """
class Message(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'timestamp' not in kwargs:
            self.timestamp = time.time_ns()


Message.set_defaults(Message, __defaults)
