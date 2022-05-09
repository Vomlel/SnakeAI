import numpy as np
import random
from deap import base, creator, tools, algorithms
from matplotlib import pyplot as plt
import functions


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # minimalizujeme počet kolizí

creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_float", random.randrange, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 10)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)


ucastnici = ["killer", "thief_vomlel", "my_tactic1", "fighter000", "fighter111", "fighter110", "fighter101", "fighter011", "fighter100", "fighter010", "fighter001"]
STEPSNUM = 20


def evaluate(genome):
    return functions.fight2(ucastnici, STEPSNUM, genome),


toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=5)

NGEN = 100  # počet generací
CXPB = 0.8  # pravděpodobnost crossoveru na páru
MUTPB = 0.7  # pravděpodobnost mutace

s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("min", np.min)

pop = toolbox.population(10)

hof = tools.HallOfFame(1)
finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=s, halloffame=hof)

print(hof[0])

mean, minimum = logbook.select("mean", "min")
fig, ax = plt.subplots()
ax.plot(range(NGEN + 1), mean, label="mean")
ax.plot(range(NGEN + 1), minimum, label="min")
ax.legend()
plt.show()