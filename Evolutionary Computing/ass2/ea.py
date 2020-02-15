import sys
sys.path.insert(0, 'evoman')

import os
import numpy as np
import custom_algorithms
import random
import copy
from demo_controller import player_controller

from environment import Environment
from deap import algorithms, base, creator, tools
from general_functions import save_pickle


experiment_name = "ea-neural-network"


class OurEnv(Environment):
    def fitness_single(self):
        return self.get_playerlife() - self.get_enemylife()

    def cons_multi(self, values):
        return values.sum() 


''' GLOBALS '''
n_hidden = 10


env_train = OurEnv(experiment_name=experiment_name,
             enemies=[5, 4, 7],
             level=2,  # integer
             playermode="ai",  # ai or human
             multiplemode="yes",
             enemymode="static",
             logs="on",
             player_controller=player_controller(n_hidden),
             speed="fastest")


n_vars = (env_train.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5


def run_train(individual):
    f, _, _, _ = env_train.play(pcont=np.asarray(individual))
    return f,


"""
CX from baseline, this cx only creates 1 child per 2 individuals
Wrap this in a tuple to avoid the errors of check_bounds
use the [:] annotation to return the kid as Individual class
According to the baseline, no cxpb is used, instead we (np.randuniform) for each crossover call
In this case, if our cxpb is equal to 0.0 we return either 1 of the parents (for selection)
We can possibly change this selection mechanism though.
"""
def baseline_cxf(ind1, ind2, cxpb, alpha=0.5):
    if cxpb != 0.0:
        alpha = np.random.uniform(0,1)
        kid = []
        for i in range(len(ind1)):
            kid.append((alpha * ind1[i]) + (1 - alpha) * ind2[i])
        kid = np.asarray(kid)
        ind2[:] = kid
        return ind2,
    else:
        choice = np.random.uniform(0,1)
        if choice < 0.5:
            return ind1,
        else:
            return ind2,


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
def ea_nn(mutation_probs, crossover_probs, pop_size=100, gens=45, sim_run_number=-1):
    lowerbound = -1
    upperbound = 1

    N_POP = pop_size
    N_GENS = gens

    ''' Register '''
    # Basic function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("evaluate", run_train)

    # Generate population of nn-biases
    toolbox.register("attr_allele", np.random.uniform, lowerbound, upperbound)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_allele, n=n_vars)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Parent selection registration
    # Changed k=N_POP due to baseline selecting as np.random.randint(0,pop.shape[0], 1), using the whole population.
    toolbox.register("selectParents", tools.selTournament, k=N_POP, tournsize=2)

    """
    See the baseline_cxf for detailed explanation of how we handle cxpb == 0.0
    """
    toolbox.register("mate", baseline_cxf)
    toolbox.decorate("mate", check_bounds(lowerbound, upperbound))

    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.decorate("mutate", check_bounds(lowerbound, upperbound))

    # Survivor selection registration
    toolbox.register("selectSurvivors", tools.selBest, k=N_POP) # delete the worst ones, keep pop size constant

    ''' Run algorithm '''
    fittest_individuals = []

    # Run only one repetition if argv, else run 10  
    N_SIMS = 1
    if sim_run_number == -1:
        N_SIMS = 10

    avgs = []
    stds = []
    mins = []
    maxs = []

    for i in range(0, N_SIMS):
        population = toolbox.population(n=N_POP)

        hof = tools.HallOfFame(1, similar=np.array_equal)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        log, fittest_individual = custom_algorithms.eaCustom(population, toolbox, cxpb=crossover_probs, mutpb=mutation_probs, ngen=N_GENS, stats=stats, halloffame=hof, verbose=True)

        fittest_individuals.append(list(fittest_individual))

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
    
    # Generate path name to save file to
    path_name = "data/"

    if(crossover_probs != 0.0):
        path_name += "cx"
    else:
        path_name += "no_cx"

    if sim_run_number >= 0:
        path_name += "_run_" + str(sim_run_number)
        save_pickle(fittest_individuals, path_name + "_individual")
        save_pickle(sts, path_name + "_stats")


if __name__ == "__main__":
    mutpb = 0.2
    cxpb = 0.5

    if(len(sys.argv) > 1):
        ea_nn(mutpb, cxpb, sim_run_number=int(sys.argv[1]))
    else:
        ea_nn(mutpb, cxpb, sim_run_number=-1)