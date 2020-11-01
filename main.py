from Evolutionary_algorithm import *
from time import time

t1 = time()

POPULATION_SIZE = 400
N_EVALUATION_STEPS = 100000
N_EPOCHS = 500
STOP_CRITERION = 20
MUTATION_CHANCE = 0.01
ELITISM_PERCENT = 0.1
TOURNAMENT_SIZE = 4
setMutationChance(MUTATION_CHANCE)

population = Population(POPULATION_SIZE,N_EVALUATION_STEPS,TOURNAMENT_SIZE,ELITISM_PERCENT)
population.initialise()
best = (population.get_best(),0)
print("Epoch 0. best score: {}, similarity to optimal: {}".format(0,best[0].score,best[0].like_optimal()))


for i in range(N_EPOCHS):
    if i - best[1] >= STOP_CRITERION:
        break
    population = population.next_generation()
    temp_best = (population.get_best(), i)
    if temp_best[0].score > best[0].score:
        best = temp_best
    print("Epoch {}. best score: {}, similarity to optimal: {}".format(i+1,temp_best[0].score,temp_best[0].like_optimal()))

population.get_best().to_file("best_strategy.txt")
print("Best strategy found scored: {}".format(population.get_best().score))
print(time()-t1)


print("Expected: {}".format(((1/3)*23*10 + (1/4)*10*10)/((23+10)*10)))
