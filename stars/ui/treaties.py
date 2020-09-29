from defaults import Defaults

__defaults = {
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def post(self, action):
        pass

Treaty.ste_defaults(Weapon, __defaults)
