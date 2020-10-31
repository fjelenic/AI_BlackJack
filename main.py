from Evolutionary_algorithm import Population
from time import time

t1 = time()

POPULATION_SIZE = 5
N_EVALUATION_STEPS = 10000
N_EPOCHS = 100000
STOP_CRITERION = 750

population = Population(POPULATION_SIZE,N_EVALUATION_STEPS)
best = (population.get_best().score,0)

for i in range(N_EPOCHS):
    if i - best[1] >= STOP_CRITERION:
        break
    crossing_candidates = population.get_crossing_candidates()
    new_unit = crossing_candidates[0].cross(crossing_candidates[1])
    new_unit.mutate().evaluate(N_EVALUATION_STEPS)
    mini_pop = crossing_candidates + [new_unit]
    population.add(mini_pop)
    temp_best = (population.get_best().score, i)
    if temp_best[0] < best[0]:
        best = temp_best
    if i % 10 == 0:
        print("Epoch {}. best score: {}".format(i,temp_best[0]))

population.get_best().to_file("best_strategy.txt")

print(time()-t1)


