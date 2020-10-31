import numpy as np
import BlackJack as bj

MUTATION_CHANCE = 0.05

class Unit:

    def __init__(self, strategy=None):
        if not strategy:
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

    def cross(self, other, method="uniform"):
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



class Population:

    def __init__(self, size, n_iterations):
        self.members=[]
        for i in range(size):
            self.members.append(Unit().evaluate(n_iterations))
        self.size = size

    def __getitem__(self, item):
        return self.members[item]

    def get_crossing_candidates(self):
        candidates = set()
        size = len(candidates)
        while size < 2:
            index = np.random.randint(len(self.members))
            candidates.add(self[index])
            if len(candidates) > size:
                size = len(candidates)
                del self.members[index]
        return list(candidates)

    def add(self,new_units):
        new_units.sort(reverse = True, key=lambda x:x.score)
        self.members += new_units[:-1]
        return self

    def get_best(self):
        return max(self.members, key=lambda x:x.score)




def setMutationChance(chance):
    global MUTATION_CHANCE
    MUTATION_CHANCE = chance