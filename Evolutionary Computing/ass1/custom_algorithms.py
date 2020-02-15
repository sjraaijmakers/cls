import random

from deap import tools, cma

def varAnd(population, toolbox, mutpb,cxpb):
    # Copy the population
    offspring = [toolbox.clone(ind) for ind in population]

    # Select parents using registered select method by DEAP
    parents = toolbox.selectParents(offspring)

    # All the parents get to mate, but no replacement to keep up diversity
    for i in range(1, len(parents), 2):
        kids = toolbox.mate(parents[i], parents[i-1], cxpb)

        for kid in kids:
            offspring.append(kid)

    # Add iterate over entire population and mutate them accroding to mutpb
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

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

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

    return population, logbook
