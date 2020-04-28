from serializable import Serializable

""" Represent 'minerals' """
class Minerals(Serializable):
    def __init__(self, **kwargs):
        self.titanium = kwargs.get('titanium', 0)
        self.lithium = kwargs.get('lithium', 0)
        self.silicon = kwargs.get('silicon', 0)
