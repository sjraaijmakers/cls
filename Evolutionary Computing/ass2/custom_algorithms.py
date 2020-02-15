import random
import numpy as np

from deap import tools, cma

def varAnd(population, toolbox, mutpb,cxpb):
    # Copy the population
    offspring = [toolbox.clone(ind) for ind in population]

    # Select parents using registered select method by DEAP
    # The default returns 2 parents
    parents = toolbox.selectParents(offspring)
    
    # Baseline method of selecting n_offspring
    # n_offspring = np.random.randint(1,3+1, 1)[0]

    # All the parents get to mate, but no replacement to keep up diversity
    # Use baseline nr_offspring to be mated, not sure about this; seems sketch
    # Delete the fitness values of the kids to let them be re-evaluated
    for i in range(1, len(parents), 2):
        # Stop after n_offspring is reached
        kids = toolbox.mate(parents[i], parents[i-1], cxpb)
        for kid in kids:
            offspring.append(kid)
            del offspring[i].fitness.values


    # Iterate over entire population and mutate them accroding to mutpb
    # Delete the fitness values of the mutated to let them be re-evaluated
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


def eaCustom(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness -> no fitness value yet (mutated and offspring)
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    fittest_individual = None

    for ind, fit in zip(invalid_ind, fitnesses):
        if fittest_individual is None:
            fittest_individual = ind

        ind.fitness.values = fit

        if fit > fittest_individual.fitness.values:
            fittest_individual = ind

    if halloffame is not None:
        halloffame.update(population)

    # Log book
    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Vary the pool of individuals (Recombination/Crossover and Mutation)
        # Do Crossover and Mutation
        offspring = varAnd(population, toolbox, mutpb,cxpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

            if fit > fittest_individual.fitness.values:
                fittest_individual = ind

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the best of offspring (survivor selection)
        best = toolbox.selectSurvivors(offspring) #
        population[:] = best

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print (logbook.stream)

    return logbook, fittest_individual
