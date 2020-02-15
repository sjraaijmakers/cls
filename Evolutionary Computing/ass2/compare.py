""" This file runs the found "fittest individuals" against all 8 enemies, 5 times
    and saves the results to a dictionary which is exported to a pickle file """

import sys
sys.path.insert(0, 'evoman')

import os
import numpy as np
import custom_algorithms
import random
from demo_controller import player_controller

from environment import Environment
from general_functions import save_pickle, open_pickle


experiment_name = "ea-neural-network"


class OurEnv(Environment):
    def fitness_single(self):
        return self.get_playerlife() - self.get_enemylife()

    def cons_multi(self, values):
        return values


n_hidden = 10


env_all = OurEnv(experiment_name=experiment_name,
             enemies=[1, 2, 3, 4, 5, 6, 7, 8],
             level=2,  # integer
             playermode="ai",  # ai or human
             multiplemode="yes",
             enemymode="static",
             logs="off",
             player_controller=player_controller(n_hidden),
             speed="fastest")


def run(individual):
    f, _, _, _ = env_all.play(pcont=np.asarray(individual))
    return f


def main(ea_type):
    fittest_individuals = open_pickle("data/" + ea_type + "_merged_individuals")

    pop_fitnesses = []

    for fi in fittest_individuals:
        ind_fitnesses = []
        for _ in range(0, 5):
            f = run(fi)
            ind_fitnesses.append(f)
        pop_fitnesses.append(ind_fitnesses)
        print(ind_fitnesses)

    stats = {
        "individuals": fittest_individuals,
        "fitnesses": pop_fitnesses
    }

    save_pickle(stats, "data/" + ea_type + "_compared_result")


if __name__ == "__main__":
    main("cx")
    main("no_cx")

