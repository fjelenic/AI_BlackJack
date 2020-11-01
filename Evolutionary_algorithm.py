import numpy as np
import BlackJack as bj

MUTATION_CHANCE = 0.05

class Unit:

    def __init__(self, strategy=None):
        if strategy is None:
            a = np.random.randint(3, size=(23, 10))
            b = np.random.randint(4, size=(10, 10))
            c = np.append(a, b, 0)
            self.strategy = c
        else:
            self.strategy = strategy
        self.score = 0

    def __repr__(self):
        return str(self.strategy)

    def __getitem__(self, item):
        return self.strategy[item]

    def action(self, my_hand, dealer_hand):
        if my_hand.soft and my_hand.pair:
            return self.strategy[-1][dealer_hand.value - 2]
        if my_hand.soft:
            return self.strategy[my_hand.value - 13 + 15][dealer_hand.value - 2]
        if my_hand.pair:
            return self.strategy[23 + int(my_hand.value/2) - 2][dealer_hand.value - 2]
        return self.strategy[my_hand.value - 5][dealer_hand.value - 2]

    def mutate(self):
        for i in range(self.strategy.shape[0]):
            for j in range(self.strategy.shape[1]):
                if np.random.random(1)[0] <= MUTATION_CHANCE:
                    if i < 23:
                        new_action = np.random.randint(3)
                        while new_action == self.strategy[i][j]:
                            new_action = np.random.randint(3)
                        self.strategy[i][j] = new_action
                    else:
                        new_action = np.random.randint(4)
                        while new_action == self.strategy[i][j]:
                            new_action = np.random.randint(4)
                        self.strategy[i][j] = new_action
        return self

    def cross(self, other, method="elitist"):
        if method == "uniform":
            break_point = 0.5
        if method == "elitist":
            break_point = self.score/(self.score + other.score)
        new_unit = Unit()
        for i in range(self.strategy.shape[0]):
            for j in range(self.strategy.shape[1]):
                if np.random.random(1)[0] < break_point:
                    new_unit[i][j] = self[i][j]
                else:
                    new_unit[i][j] = other[i][j]
        return new_unit

    def evaluate(self, n_iterations):
        game = bj.Game()
        for i in range(n_iterations):
            game.play(self)
        return self

    def to_file(self, file):
        with open(file, 'w') as f:
            f.write(str(self))

    def like_optimal(self):
        opt = Unit(np.array([[0,0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0,0,0],
                             [0,2,2,2,2,0,0,0,0,0],
                             [2,2,2,2,2,2,2,2,0,0],
                             [2,2,2,2,2,2,2,2,2,0],
                             [0,0,1,1,1,0,0,0,0,0],
                             [1,1,1,1,1,0,0,0,0,0],
                             [1,1,1,1,1,0,0,0,0,0],
                             [1,1,1,1,1,0,0,0,0,0],
                             [1,1,1,1,1,0,0,0,0,0],
                             [1,1,1,1,1,1,1,1,1,1],
                             [1,1,1,1,1,1,1,1,1,1],
                             [1,1,1,1,1,1,1,1,1,1],
                             [0,0,0,2,2,0,0,0,0,0],
                             [0,0,0,2,2,0,0,0,0,0],
                             [0,0,2,2,2,0,0,0,0,0],
                             [0,0,2,2,2,0,0,0,0,0],
                             [0,2,2,2,2,0,0,0,0,0],
                             [1,2,2,2,2,1,1,0,0,0],
                             [1,1,1,1,1,1,1,1,1,1],
                             [1,1,1,1,1,1,1,1,1,1],
                             [3,3,3,3,3,3,0,0,0,0],
                             [3,3,3,3,3,3,0,0,0,0],
                             [0,0,0,3,3,0,0,0,0,0],
                             [2,2,2,2,2,2,2,2,0,0],
                             [3,3,3,3,3,0,0,0,0,0],
                             [3,3,3,3,3,3,0,0,0,0],
                             [3,3,3,3,3,3,3,3,3,3],
                             [3,3,3,3,3,1,3,3,1,1],
                             [1,1,1,1,1,1,1,1,1,1],
                             [3,3,3,3,3,3,3,3,3,3]]))
        summation = 0
        for i in range(opt.strategy.shape[0]):
            for j in range(opt.strategy.shape[1]):
                if opt[i][j] == self[i][j]:
                    summation += 1
        return summation/((23+10)*10)



class Population:

    def __init__(self, size, n_iterations, tournament_size, elitism_percent):
        self.members=[]
        self.size = size
        self.n_iterations = n_iterations
        self.tournament_size = tournament_size
        self.elitism_percent = elitism_percent

    def __getitem__(self, item):
        return self.members[item]

    def initialise(self):
        for i in range(self.size):
            self.add(Unit().evaluate(self.n_iterations))

    def tournament_selection(self, N):
        candidates = set()
        while len(candidates) < N:
            index = np.random.randint(self.size)
            candidates.add(self[index])
        return max(candidates, key=lambda x:x.score)

    def add(self, unit):
        lo = 0
        hi = len(self.members)
        if hi == 0:
            return self.members.append(unit)
        if hi == 1:
            if unit.score > self[0].score:
                self.members = [unit] + self.members
            else:
                self.members.append(unit)
            return
        while lo < hi:
            mid = (lo + hi) // 2
            if unit.score > self.members[mid].score and unit.score < self.members[mid-1].score:
                break
            if unit.score > self.members[mid].score:
                hi = mid
            else:
                lo = mid + 1
        self.members = self.members[:mid] + [unit] + self.members[mid:]
        return self

    def next_generation(self):
        new_population = Population(self.size,self.n_iterations,
                                    self.tournament_size,self.elitism_percent)
        new_population.members = self.members[:round(self.size*self.elitism_percent)]
        while len(new_population.members) < self.size:
            unit1 = self.tournament_selection(self.tournament_size)
            unit2 = self.tournament_selection(self.tournament_size)
            new_unit = unit1.cross(unit2).evaluate(self.n_iterations)
            new_population.add(new_unit)
        return new_population

    def get_best(self):
        return self.members[0]




def setMutationChance(chance):
    global MUTATION_CHANCE
    MUTATION_CHANCE = chance