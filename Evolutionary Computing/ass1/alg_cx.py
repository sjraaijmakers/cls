import sys
sys.path.insert(0, 'evoman')

import os
import numpy as np
import custom_algorithms
import random
from demo_controller import player_controller

from environment import Environment
from deap import algorithms, base, creator, tools
from general_functions import save_pickle

experiment_name = "ea-neural-network"
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)


class OurEnv(Environment):
    def fitness_single(self):
        return self.get_playerlife() - self.get_enemylife()


''' GLOBALS '''
enemy = 4
n_hidden = 10


env = OurEnv(experiment_name=experiment_name,
             enemies=[enemy],
             level=2,  # integer
             playermode="ai",  # ai or human
             enemymode="static",
             logs="off",
             player_controller=player_controller(n_hidden),
             speed="fastest")

n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5

# Fitness function / evaluate function
def run_sim_function(individual):
    f, p, e, t = env.play(pcont=np.asarray(individual))
    return f,


# Blended function (is now blended crossover)
def blended_cxf(ind1, ind2, cxpb):
    alpha = 0.5
    if random.random() < cxpb:
        for i, (x1, x2) in enumerate(zip(ind1, ind2)):
                gamma = (1. + 2. * alpha) * random.random() - alpha
                ind1[i] = (1. - gamma) * x1 + gamma * x2
                ind2[i] = gamma * x1 + (1. - gamma) * x2
    return ind1, ind2

# Function to set min and max value of allele
def check_bounds(min, max):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrapper
    return decorator

# Actual algorithm
def ea_nn(mutation_probs, crossover_probs, sim=-1):
    lowerbound = -1
    upperbound = 1

    # FLEXIBLE PARAMS
    N_POP = 100 # keep this number even
    N_GEN = 30

    N_SIMS = 1
    if sim == -1:
        N_SIMS = 10

    ''' Register '''
    # Basic function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("evaluate", run_sim_function)

    # Generate population of nn-biases
    toolbox.register("attr_allele", np.random.uniform, lowerbound, upperbound)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_allele, n=n_vars)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Parent selection registration
    toolbox.register("selectParents", tools.selTournament, k=int(N_POP/2), tournsize=2)

    # Recombination registration
    toolbox.register("mate", blended_cxf)
    toolbox.decorate("mate", check_bounds(lowerbound, upperbound))

    # Mutation TODO: possibly change for self adaptive mutation? pg 57 book
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.decorate("mutate", check_bounds(lowerbound, upperbound))

    # Survivor selection registration
    toolbox.register("selectSurvivors", tools.selBest, k=N_POP) # delete the worst ones, keep pop size constant

    ''' Run algorithm '''
    avgs = []
    stds = []
    mins = []
    maxs = []

    # Run N simulations
    for i in range(0, N_SIMS):
        population = toolbox.population(n=N_POP)

        hof = tools.HallOfFame(1, similar=np.array_equal)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        final_population, log = custom_algorithms.eaCustom(population, toolbox, cxpb=crossover_probs, mutpb=mutation_probs, ngen=N_GEN, stats=stats, halloffame=hof, verbose=True)

        gen, avg, nevals, std, min_f, max_f = log.select("gen", "avg", "nevals", "std", "min", "max")

        avgs.append(avg)
        stds.append(std)
        mins.append(min_f)
        maxs.append(max_f)

    sts = {
        "gen": gen,
        "avg": avgs,
        "std": stds,
        "min": mins,
        "max": maxs
    }

    save_pickle(sts, 'e3/NN_crosover_run_' + str(sim), enemy, mutation_probs, crossover_probs, N_SIMS, N_POP, N_GEN)


if __name__ == "__main__":
    # These params are fixed now, according to param tuning results
    mutation_probs = 0.1
    crossover_probs = 0.9
    ea_nn(float(mutation_probs), float(crossover_probs), sim=sys.argv[1])
