import cargo

""" Planet class """
class Planet:
    """ Number of clicks of the planet's temperature """
    """ Range of -15 to 115 """
    __temp = 0

    """ todo """
    __on_surface = cargo.Cargo()

    """ List of gravity values for display (0..100) """
    __grav_values = [0.20, 0.22, 0.23, 0.24, 0.26, 0.28, 0.29, 0.30, 0.32, 0.34, 0.35, 0.36, 0.38, 0.40, 0.41, 0.42, 0.44, 0.46, 0.47, 0.48, 0.50, 0.52, 0.53, 0.54, 0.56, 0.57, 0.59, 0.60, 0.62, 0.64, 0.65, 0.67, 0.68, 0.70, 0.71, 0.73, 0.74, 0.75, 0.77, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.60, 1.64, 1.68, 1.72, 1.76, 1.80, 1.84, 1.88, 1.92, 1.96, 2.00, 2.11, 2.22, 2.33, 2.44, 2.55, 2.66, 2.77, 2.88, 3.00, 3.12, 3.24, 3.36, 3.48, 3.60, 3.72, 3.84, 3.96, 4.09, 4.22, 4.35, 4.48, 4.61, 4.74, 4.87, 5.00]
    
    """ Restore class from a string """
    def __init__(self, from_string):
        pass

    """ Create an empty class """
    def __init__(self):
        pass

    """ Grow the current population """
    def grow_population(self):
        planetvalue = float(self.calchab())
        pop = self.__on_sirface.people
        rate = self.rate
        maxpop = self.maxpop
        try:
            pop = int(pop)
        except ValueError:
            return 0
        if pop <= 0:
            return 0
        try:
            rate = float(rate)
        except ValueError:
            return pop
        try:
            maxpop = float(maxpop)
        except ValueError:
            maxpop = 1000000
        try:
            planetvalue = float(planetvalue)
        except ValueError:
            planetvalue = 0.00
        maxpop *= planetvalue
        h = maxpop/2.0
        g = float(float(maxpop)/float(h+pop))/2.0
        rate = (g*rate)
        if pop < maxpop:
            pop *= (rate + 1.0)
            if pop > maxpop:
                pop = maxpop
        elif pop > maxpop:
            pop *= (-rate + 1.0)
            if pop < maxpop:
                pop = maxpop
        self.__on_surface.people = int(round(pop, -2))


    """ Return the planet temperature (-260C to 260C) """
    def display_temp(self):
        return str(self.__temp * 4 - 200) + 'C'

    """ Document me """
    def display_grav(self):
        return str(self._grav_values[self.grav]) + 'g'
    
    def __init__(self, rad, temp, grav, pop, posx, posy, rate, maxpop, radrange, temprange, gravrange):
        self.rad = int(rad)
        self.temp = int(temp)
        self.grav = int(grav)
        self.pop = int(pop)
        self.posx = int(posx)
        self.posy = int(posy)
        self.rate = float(rate)
        self.maxpop = int(maxpop)
        self.radr = sorted(radrange)
        self.tempr = sorted(temprange)
        self.gravr = sorted(gravrange)

    """ Calculate the planet's value for the current player (-60 to 100) """
    """ value = SQRT[(1-g)^2+(1-t)^2+(1-r)^2]*(1-x)*(1-y)*(1-z)/SQRT[3] """
    """ where x=g-1/2 for g>1/2 | x=0 for g<1/2 | y=t-1/2 for t>1/2 | y=0 for t<1/2 | z=r-1/2 for r>1/2 | z=0 for r<1/2 """
    def calc_planet_value(self):
        if not (self.rad in range(self.radr[0], self.radr[1]) and self.temp in range(self.tempr[0], self.tempr[1]) and self.grav in range(self.gravr[0], self.gravr[1])):
            a = (self.radr[1]-self.radr[0])/2
            r = abs((a+self.radr[0])-self.rad)-a
            #print(r)
            if r > 20:
                r = 20
            a = (self.tempr[1]-self.tempr[0])/2
            t = abs((a+self.tempr[0])-self.temp)-a
            if t > 20:
                t = 20
            a = (self.gravr[1]-self.gravr[0])/2
            g = abs((a+self.gravr[0])-self.grav)-a
            if g > 20:
                g = 20
            return -(r+t+g)/100
        else:
            a = (self.radr[1]-self.radr[0])/2
            r = ((a+self.radr[0])-self.rad)/a
            #print(r)
            if r < 0:
                r = -r
            a = (self.tempr[1]-self.tempr[0])/2
            t = ((a+self.tempr[0])-self.temp)/a
            if t < 0:
                t = -t
            a = (self.gravr[1]-self.gravr[0])/2
            g = ((a+self.gravr[0])-self.grav)/a
            if g < 0:
                g = -g
            if g > 1/2:
                x = g-1/2
            else:
                x = 0
            if t > 1/2:
                y = t-1/2
            else:
                y = 0
            if r > 1/2:
                z = r-1/2 
            else:
                z = 0
            #print(x)
            #print(y)
            #print(z)
            return float((((1-g)**2+(1-t)**2+(1-r)**2)**0.5)*(1-x)*(1-y)*(1-z)/(3**0.5))
    #def transferpop(self, otherplanet, amount):
    #    for i in range(amount):
    #        if self.pop == 0:
    #            break
    #        self.pop -= 1
    #        otherplanet.pop += 1
    


""" Test the Planet class """
def _test():
    print('planet._test - begin')
    _test_grow_population()
    print('planet._test - end')

""" Test the Planet.grow_population method """
def _test_grow_population():
    print('planet._test_grow_population - begin')
    p = Planet()
    p.grow_population()
    print('planet._test_grow_population - end')
