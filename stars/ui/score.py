from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'score_table': [],
    # Chart
    'score_chart_type': 'Energy',
    'options_score_chart_type': ['Planets', 'Energy', 'Tech Levels', 'Minerals', 'Facilities', 'Unarmed Ships', 'Escort Ships', 'Ships of the Wall', 'Starbases', 'Score'],
    'score_chart': [],
}

""" Converion of type into key """
FIND_MATCH = {
    'Planets': 'planets',
    'Energy': 'energy',
    'Tech Levels': 'tech_levels',
    'Minerals': 'minerals',
    'Facilities': 'facilities',
    'Unarmed Ships': 'ships_unarmed',
    'Escort Ships': 'ships_escort',
    'Ships of the Wall': 'ships_of_the_wall',
    'Starbases': 'starbases',
    'Score': 'score'
}

""" Components of score are precomputed as part of turn generation """
class Score(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        self.score_table = ['<th class="score_vertical"></th>']
        for field in self.options_score_chart_type:
            self.score_table[0] += '<th class="score_vertical">' + field + '</th>' #TODO make vertical headers, add more columns
        self.score_table[0] += '<th class="score_vertical">Rank</th>' #TODO make vertical headers, add more columns
        # Show self first
        self.score_row(self.player.get_intel(reference=self.player))
        self.add_to_score_chart(self.player.get_intel(reference=self.player), True)
        for (player, intel) in self.player.get_intel(by_type='Player').items():
            if player != self.player:
                print(intel)
                self.score_row(intel)
                self.add_to_score_chart(intel)

    """ Take intel data and make it into a score row """
    def score_row(self, intel):
        self.score_table.append('<td>' + intel.name + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('planets', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('energy', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('tech_levels', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('minerals', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('facilities', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('ships_unarmed', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('ships_escort', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('ships_of_the_wall', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('starbases', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('score', '?')) + '</td><td style="text-align: center">'
            + '{:.0f}'.format(intel.get('score_rank', '?')) + '</td>')

    def add_to_score_chart(self, intel, is_self=False):
        if len(self.score_chart) < 4:
            self.score_chart = [[], [], [], []]
        key = FIND_MATCH[self.score_chart_type]
        data = {}
        for i in range(3000, int(float(self.player.date))+1):
            if is_self:
                self.score_chart[0].append(str(i)+'.00')
            if str(i)+'.00' not in intel[key].keys():
                data[str(i)+'.00'] = 0
            else:
                data[str(i)+'.00'] = intel[key][str(i)+'.00']
        self.score_chart[1].append(intel.name)
        self.score_chart[2].append(data)
        self.score_chart[3].append(intel['color'])
        print(self.score_chart)
        

Score.set_defaults(Score, __defaults, sparse_json=False)
