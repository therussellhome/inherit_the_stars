from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    # Alerts/errors to send back to the player
    'user_alerts': [],
}


""" Provide a base class for sending alerts/errors to the user """
class UI(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


UI.set_defaults(UI, __defaults, sparse_json=False)
