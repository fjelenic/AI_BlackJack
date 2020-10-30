import numpy as np
import BlackJack as bj

MUTATION_CHANCE = 0.05

class Unit:

    def __init__(self):
        a = np.random.randint(3, size=(23, 10))
        b = np.random.randint(4, size=(10, 10))
        c = np.append(a, b, 0)
        self.strategy = c
        self.score = 0

    def __repr__(self):
        return str(self.strategy)

    def __getitem__(self, item):
        return self.strategy[item]

    def action(self, my_hand, dealer_hand):
        if my_hand.soft and my_hand.pair:
            return self.strategy[-1][dealer_hand.value - 2]
        if my_hand.soft:
            return self.strategy[my_hand.value - 3 + 15][dealer_hand.value - 2]
        if my_hand.pair:
            return self.strategy[23 + int(my_hand.value/2) - 1][dealer_hand.value - 2]
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

    def evaluate(self,n_iterations):
        for i in range(n_iterations):
            game = bj.Game()
            game.play(self)






def setMutationChance(chance):
    global MUTATION_CHANCE
    MUTATION_CHANCE = chance