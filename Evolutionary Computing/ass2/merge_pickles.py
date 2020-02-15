from general_functions import save_pickle, open_pickle


def merge_runs(ea_type):
    n = 10
    population = []

    for i in range(n):
        individual = open_pickle("data/" + ea_type + "_run_" + str(i) + "_individual")[0]
        population.append(individual)    
        
    save_pickle(population, "data/" + ea_type + "_merged_individuals")


def merge_stats(ea_type):
    n = 10

    avgs = []
    maxs = []

    for i in range(n):
        stats = open_pickle("data/" + ea_type + "_run_" + str(i) + "_stats")
        avgs.append(stats["avg"][0])
        maxs.append(stats["max"][0])

    sts = {
        "gen": stats["gen"],
        "avg": avgs,
        "max": maxs
    }

    save_pickle(sts, "data/" + ea_type + "_merged_stats") 


if __name__ == "__main__":
    merge_runs("cx")
    merge_stats("cx")

    merge_runs("no_cx")
    merge_stats("no_cx")