import to_json

""" Represent 'minerals' """
class Minerals(to_json.Serializable):
    def __init__(self, **kwargs):
        self.titanium = kwargs.get('titanium', 0)
        self.lithium = kwargs.get('lithium', 0)
        self.silicon = kwargs.get('silicon', 0)
