from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'date': '',
    'sender': Reference('Player/'),
    'receiver': Reference('Player/'),
    'message': '',
    'parameters': [],
    'action': '',
    'star': False,
    'read': False,
}


""" Message from game, minister, or other player """
class Message(Defaults):
    pass

Message.set_defaults(Message, __defaults)
