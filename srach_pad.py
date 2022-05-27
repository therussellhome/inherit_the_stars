""" get the time needed to get all the materials for a production queue item. """
def time_til_done(self, queue, i):
    ti = 0
    li = 0
    si = 0
    yj = 0
    pro = 0
    # get what is needed
    for j in range(len(queue)):
        item = queue[j]
        yj += item.cost.energy
        if item.planet == self:
            ti += item.cost.ti
            li += item.cost.li
            si += item.cost.si
            pro += item.cost.ti + item.cost.li + item.cost.si
        if j == i:
            break
    # calculate the time needed to get what is needed
    t_ti = (ti - self.on_surface.titanium) / (self.mineral_availability('titanium') * self._operate('mines'))
    t_li = (li - self.on_surface.lithium) / (self.mineral_availability('lithium') * self._operate('mines'))
    t_si = (si - self.on_surface.silicon) / (self.mineral_availability('silicon') * self._operate('mines'))
    t_yj = (yj - (self.player.energy * self.player.finance_constuction_percent / 100)) / (self.player.prodict_budgit() * self.player.finance_constuction_percent / 100)
    t_pro = pro / 1 + self._operate('factories') * self.player.tech_level.construction * 1234
    return (t_ti, t_li, t_si, t_yj, t_pro)

