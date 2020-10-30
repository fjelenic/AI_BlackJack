import Evolutionary_algorithm as ea
import BlackJack as bj

POPULATION_SIZE = 5
N_EVALUATION_STEPS = 10000

population = []
for i in range(POPULATION_SIZE):
    population.append(ea.Unit())

for i in range(POPULATION_SIZE):
    population[i].evaluate(N_EVALUATION_STEPS)

print([p.score for p in population])


