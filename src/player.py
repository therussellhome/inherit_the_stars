from . import game_engine
from .cost import Cost
from .defaults import Defaults
from .minister import Minister
from .race import Race
from .reference import Reference

""" Default values (default, min, max)  """
__defaults = {
    'race': [Race()],
    'ministers': [[Minister(name='default')]]
}

""" the class to build the player """
class Player(Defaults):
    """ the line is a string that contains all the player data """
    def __init__(self, **kwargs):
        """
        sets = line.strip().split(", ")
        self.name = sets[0]
        self._energy = int(sets[1])
        self._effort = int(sets[2])
        self.factory_efficency = int(sets[3])
        self.mine_efficency = int(sets[4])
        self.effort_efficency = int(sets[5])
        self.tax_rate = int(sets[6])
        self.research_rate = int(sets[7])
        self.stimulus_package = int(sets[8])
        self.research_level = int(sets[9])
        s_set = sets[10].split(",")
        self.factory_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[11].split(",")
        self.mine_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[12].split(",")
        self._research_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[13].split(",")
        self._origanal_research_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        self._research_queue = [[self._research_cost.energy, self._research_cost.effort], [self._origanal_research_cost.energy * (2+self.research_level/2), self._origanal_research_cost.effort * (2+self.research_level/2)]]
        """
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Player_' + str(id(self))
        game_engine.register(self)
    
    """ takes the turn """
    def take_turn(self):
        self.doResearch()
        self.__effort = 0

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


Player.set_defaults(Player, __defaults)
