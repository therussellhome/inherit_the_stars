import game_engine

""" Represent 'minerals' """
class Minerals:
    def __init__(self, **kwargs):
        self.titanium = kwargs.get('titanium', 0)
        self.lithium = kwargs.get('lithium', 0)
        self.silicon = kwargs.get('silicon', 0)

# Register the class with the game engine
game_engine.register_class(Minerals)
