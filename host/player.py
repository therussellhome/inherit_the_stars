from . import game_engine
from .cost import Cost
from .minister import Minister
from .race import Race

""" Default values (default, min, max)  """
__defaults = {
    'race': [Race()],
    'ministers': [[Minister(name='default')]]
}

""" the class to build the player """
class Player(game_engine.Defaults):
    """ the line is a string that contains all the player data """
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Player_' + str(id(self))
        game_engine.register(self)
    
    """ takes the turn """
    def take_turn(self):
        self.doResearch()

    """ research """
    def do_research(self):
        """ if research queue is empty fill it up """
        if len(self._research_queue) < 1:
            self._research_queue.append([int(self._origanal_research_cost.energy * (1+self.research_level/2)), int(self._origanal_research_cost.effort * (1+self.research_level/2)), 0])
        if len(self._research_queue) < 2:
            self._research_queue.append([int(self._origanal_research_cost.energy * (2+self.research_level/2)), int(self._origanal_research_cost.effort * (2+self.research_level/2)), 0])
        for i in range(100):
            """ do reasearch """
            if self._energy >= self._research_cost.energy:
                self._energy -= self._research_cost.energy
                self._research_cost.energy = 0
            else:
                self._research_cost.energy -= self._energy
                self._energy = 0
            
            if self._effort >= self._research_cost.effort:
                self._effort -= self._research_cost.effort
                self._research_cost.effort = 0
            else:
                self._research_cost.effort -= self._effort
                self._effort = 0
            
            if self._research_cost.energy == 0 and self._research_cost.effort == 0:
                self._research_level += 1
                self._research_queue.pop(0)
                self._research_cost.energy = int(self._research_queue[0][0])
                self._research_cost.effort = int(self._research_queue[0][1])
                self._research_queue.append([int(self._origanal_research_cost.energy * (2+self.research_level/2)), int(self._origanal_research_cost.effort * (2+self.research_level/2)), 0])
            else:
                self._research_queue[0] = [int(self._research_cost.energy), int(self._research_cost.effort)]
                break

# Register the class with the game engine
game_engine.register(Player, defaults=__defaults)
