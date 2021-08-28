from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'score_table': [],
    # Chart
    'score_chart_type': 'Economy',
    'options_score_chart_type': ['Planets', 'Ships', 'Economy'],
    'score_chart': [],
}


""" Components of score are precomputed as part of turn generation """
class Score(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        self.score_table = ['<th></th><th>Energy</th><th>Planets</th><th>Starbases</th>'] #TODO make vertical headers, add more columns
        # Show self first
        self.score_row(self.player().get_intel(reference=self.player()))
        for (player, intel) in self.player().get_intel(by_type='Player').items():
            if player != self.player():
                self.score_row(intel)

    """ Take intel data and make it into a score row """
    def score_row(self, intel):
        self.score_table.append('<td>' + intel.name + '</td><td style="text-align: right">'
                + str(intel.get('energy', '?')) + '</td><td style="text-align: right">'
                + str(intel.get('planets', '?')) + '</td><td style="text-align: right">'
                + str(intel.get('starbases', '?')) + '</td>')

Score.set_defaults(Score, __defaults, sparse_json=False)
