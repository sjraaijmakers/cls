import numpy as np
from network import Network
from sa import SA
import pandas as pd
from pickles import save_pickle
from circle import Circle
import multiprocessing


def run_experiment(experiment_name, network, alpha, edit_type, n, mcls, temps, cooling_schedules, reps=10):
    d_ns = []
    d_costs = []
    d_temps = []
    d_alphas = []
    d_ls = []
    d_cs = []
    d_init_temps = []
    
    print("Run " + experiment_name + " for " + network.name + " with " + str(reps) + " reps.")

    for start_temp in temps:
        for cooling_schedule in cooling_schedules:
            for mcl in mcls:
                for _ in range(reps):
                    ns, costs, temps, _ = SA(network).run(start_temp, alpha, edit_type, n, mcl, cooling_schedule=cooling_schedule)

                    d_ns += ns
                    d_costs += costs
                    d_temps += temps
                    d_alphas += [alpha] * len(ns)
                    d_ls += [mcl] * len(ns)
                    d_cs += [cooling_schedule] * len(ns)
                    d_init_temps += [start_temp] * len(ns)

                    print("L: " + str(mcl) + "\tT0: " + str(start_temp) + "\tcooling_schedule: " + cooling_schedule + 
                          "\tinitial cost: " + str(costs[0]) + "\tfinal cost: " + str(costs[-1]))

    dt = {
        "n": d_ns,
        "cost": d_costs,
        "temp": d_temps,
        "alpha": d_alphas,
        "l": d_ls,
        "cooling_schedule": d_cs,
        "init_temp": d_init_temps
    }

    df = pd.DataFrame().from_dict(dt)

    save_pickle(df, "data/" + network.name + "_" + experiment_name)

# Different cooling schedules
def run_TSP_exp_cs():
    filename = "a280"
    network = Network("routes/" + filename)
    start_temp = 80
    alpha = 0.99
    number_of_markov_chains = 1000
    cooling_schedules = ["exponential", "linear"]
    mcls = [300]
    reps = 5

    run_experiment("cooling_schedules", network, alpha, "2-opt", number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)


# Different l
def run_TSP_exp_mcls():
    filename = "a280"
    network = Network("routes/" + filename)

    start_temp = 80
    alpha = 0.99
    number_of_markov_chains = 1000
    cooling_schedules = ["exponential"]
    mcls = [100, 200, 300, 400, 500]
    reps = 5

    run_experiment("mcls", network, alpha, "2-opt", number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)


# Different initial temps
def run_TSP_exp_temps():
    filename = "a280"
    network = Network("routes/" + filename)

    temps = [30, 50, 80]
    alpha = 0.99
    number_of_markov_chains = 1000
    cooling_schedules = ["exponential"]
    mcls = [300]
    reps = 5

    run_experiment("temps", network, alpha, "2-opt", number_of_markov_chains, mcls, temps, cooling_schedules, reps=reps)


def run_CIR_exp_cs(N):
    circle = Circle(N)
    start_temp = 80
    alpha = 0.99
    number_of_markov_chains = 1000
    mcls = [300]
    cooling_schedules = ["exponential", "linear"]
    reps = 5

    edit_types = {
        1: "random_gen",
        2: "pertubate_points",
        3: "pertubate_force"
    }

    run_experiment("cooling_schedules", circle, alpha, edit_types[2], number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)

def run_CIR_exp_mcls(N):
    circle = Circle(N)
    start_temp = 80
    alpha = 0.99
    number_of_markov_chains = 1000
    cooling_schedules = ["exponential"]
    mcls = [100, 200, 300, 400, 500]
    reps = 5

    edit_types = {
        1: "random_gen",
        2: "pertubate_points",
        3: "pertubate_force"
    }

    run_experiment("mcls", circle, alpha, edit_types[2], number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)

def run_CIR_exp_edit_types(N):
    circle = Circle(N)
    start_temp = 80
    alpha = 0.99
    number_of_markov_chains = 1000
    cooling_schedules = ["exponential"]
    mcls = [300]
    reps = 5

    edit_types = {
        1: "random_gen",
        2: "pertubate_points",
        3: "pertubate_force"
    }

    run_experiment("edit_type_" + str(edit_types[2]) , circle, alpha, edit_types[2], number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)
    run_experiment("edit_type_" + str(edit_types[3]) , circle, alpha, edit_types[3], number_of_markov_chains, mcls, [start_temp], cooling_schedules, reps=reps)

if __name__ == "__main__":
    # run_TSP_exp_cs()
    # run_TSP_exp_mcls()
    # run_TSP_exp_temps()

    # jobs = []
    N = 6
    # run_CIR_exp_cs(N)
    # run_CIR_exp_mcls(N)
    # run_CIR_exp_edit_types(N)