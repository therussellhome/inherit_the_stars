from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'score_player01': [''],
    'score_player02': [''],
    'score_player03': [''],
    'score_player04': [''],
    'score_player05': [''],
    'score_player06': [''],
    'score_player07': [''],
    'score_player08': [''],
    'score_player09': [''],
    'score_player10': [''],
    'score_player11': [''],
    'score_player12': [''],
    'score_player13': [''],
    'score_player14': [''],
    'score_player15': [''],
    'score_player16': [''],
    'score_planets01': [''],
    'score_planets02': [''],
    'score_planets03': [''],
    'score_planets04': [''],
    'score_planets05': [''],
    'score_planets06': [''],
    'score_planets07': [''],
    'score_planets08': [''],
    'score_planets09': [''],
    'score_planets10': [''],
    'score_planets11': [''],
    'score_planets12': [''],
    'score_planets13': [''],
    'score_planets14': [''],
    'score_planets15': [''],
    'score_planets16': [''],
    'score_ships01': [''],
    'score_ships02': [''],
    'score_ships03': [''],
    'score_ships04': [''],
    'score_ships05': [''],
    'score_ships06': [''],
    'score_ships07': [''],
    'score_ships08': [''],
    'score_ships09': [''],
    'score_ships10': [''],
    'score_ships11': [''],
    'score_ships12': [''],
    'score_ships13': [''],
    'score_ships14': [''],
    'score_ships15': [''],
    'score_ships16': [''],

    # Chart
    'score_chart': ['Economy'],
    'options_score_chart': [['Planets', 'Ships', 'Economy']],
}


""" Components of score are precomputed as part of turn generation """
class Score(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Show self first
        my_reference = 'PlayerUI/' + self.player.name
        self.copy_score(1, self.player.get_intel(my_reference))
        self.set(1, 'player', self.player.name)
        i = 2
        for intel in self.player.get_intel('PlayerUI'):
            if intel.reference != my_reference:
                self.copy_score(i, intel)
                i += 1

    """ Copy the score for a player """
    def copy_score(self, player, intel):
        key = 'score_{}{:02d}'
        self.__dict__[key.format('player', player)] = intel.reference.split('/')[1]
        elements = ['planets', 'ships']
        for attribute in elements:
            self.__dict__[key.format(attribute, player)] = intel.get(attribute, default='?')

Score.set_defaults(Score, __defaults)
