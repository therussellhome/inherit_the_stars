import minerals

""" Represent 'cargo' that can be held """
""" A cargo_max of -1 is used to indicate no maximum """
class Cargo(minerals.Minerals):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.people = kwargs.get('people', 0)
        self.cargo_max = kwargs.get('cargo_max', -1)
