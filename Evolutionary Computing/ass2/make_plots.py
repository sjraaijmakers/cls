""" This file processes the data generated in compare.py """


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from general_functions import open_pickle, save_pickle

from itertools import cycle

ENEMY_MAP = {
        1: "Flashman",
        2: "Airman",
        3: "Woodman",
        4: "Heatman",
        5: "Metalman",
        6: "Crashman",
        7: "Bubbleman",
        8: "Quickman"
}

# CX = BLUE
# NO_CX = ORANGE

sns.set(font_scale=2)

color_cycle = cycle(["C0", "C1"])

def evol_time():
    algs = ["cx", "no_cx"]

    fig, ax = plt.subplots()

    for alg in algs:
        c = next(color_cycle)
        stats = open_pickle("data/" + alg + "_merged_stats")
        plt.plot(stats["gen"], np.amax(stats["max"], axis=0), ".", color=c, alpha=0.8)
        plt.plot(stats["gen"][np.argmax(np.amax(stats["max"], axis=0))], np.max(np.amax(stats["max"], axis=0)), "x", markersize=20, color=c)
        plt.errorbar(stats["gen"], np.mean(stats["avg"], axis=0),  yerr=np.std(stats["avg"], axis=0), label=alg, color=c)

    fig.tight_layout()
    plt.xlabel("Generation")
    plt.ylabel("Gain")
    plt.legend()
    plt.savefig("evolution-over-time.pdf")
    plt.show()

def boxplot():
    algs = ["cx", "no_cx"]
    df_all = pd.DataFrame()

    for alg in algs:
        color = next(color_cycle)
        stats = open_pickle("data/" + alg + "_compared_result")
        df_tmp = pd.DataFrame()
        df_tmp["Gain"] = np.sum(np.mean(stats["fitnesses"], axis=1), axis=1)        
        df_tmp["Alg"] = alg
        df_all = pd.concat([df_all, df_tmp])

    fig, ax = plt.subplots()
    ax = sns.boxplot(x="Alg", y="Gain", data=df_all)
    fig.tight_layout()
    plt.savefig("box-plot.pdf")
    plt.show()


def get_best(save=False):
    algs = ["cx", "no_cx"]

    for alg in algs:
        all_gains = []
        all_wins = []

        print(alg)

        stats = open_pickle("data/" + alg + "_compared_result")
        for i, s in enumerate(stats["fitnesses"]):
            avg_fitness = np.mean(s, axis=0)
            gain = np.sum(avg_fitness)
            wins = np.sum(avg_fitness >= 0)

            all_gains.append(gain)
            all_wins.append(wins)

            print(i, avg_fitness, gain, wins)

        highest_gain = np.argmax(all_gains)
        most_wins = np.argmax(all_wins)

        print("Highest gain: run " + str(highest_gain) + ", most wins: run " + str(most_wins))
        
        if save:
            np.savetxt("data/" + alg + "_highest_gain.txt", highest_gain)
            np.savetxt("data/" + alg + "_most_wins.txt", most_wins)


def best_fitnesses_barplot():
    stats_cx = open_pickle("data/cx_compared_result")
    stats_no_cx = open_pickle("data/no_cx_compared_result")

    # hardcoded!!!
    cx_hg = np.mean(stats_cx["fitnesses"][6], axis=0)
    cx_mw = np.mean(stats_cx["fitnesses"][4], axis=0)
    no_cx_hg = np.mean(stats_no_cx["fitnesses"][2], axis=0)
    no_cx_mw = np.mean(stats_no_cx["fitnesses"][2], axis=0)

    best = [cx_hg, cx_mw, no_cx_hg, no_cx_mw]

    df_all = pd.DataFrame()

    for i, b in enumerate(best):
        df_tmp = pd.DataFrame()
        df_tmp["Fitness"] = b
        df_tmp["Enemy"] = np.arange(8) + 1
        df_tmp["Enemy_name"] = df_tmp["Enemy"].map(ENEMY_MAP)

        if i == 0:
            alg_type = "CX (highest_gain)"
        elif i == 1:
            alg_type = "CX (most wins)"
        elif i == 2:
            alg_type = "No CX (highest gain)"
        elif i == 3:
            alg_type = "No CX (most wins)"

        df_tmp["Alg_type"] = alg_type

        df_all = pd.concat([df_all, df_tmp])

    print(df_all)
    fig, ax = plt.subplots()
    sns.barplot(x="Enemy", y="Fitness", hue="Alg_type", palette=["C0", "C4", "C1", "C3"], data=df_all)
    fig.tight_layout()
    plt.savefig("bar-plot.pdf")
    plt.show()


def table_best():
    stats_cx = open_pickle("data/cx_compared_result")
    stats_no_cx = open_pickle("data/no_cx_compared_result")

    # hardcoded!!!
    cx_hg = np.mean(stats_cx["fitnesses"][6], axis=0)
    cx_mw = np.mean(stats_cx["fitnesses"][4], axis=0)
    no_cx_hg = np.mean(stats_no_cx["fitnesses"][2], axis=0)
    no_cx_mw = np.mean(stats_no_cx["fitnesses"][2], axis=0)

    print("CX highest gain: " + str(cx_hg))
    print("CX most wins: " + str(cx_mw))
    print("No CX highest gain: " + str(no_cx_hg))
    print("No CX most wins: " + str(no_cx_mw))


if __name__ == "__main__":
    evol_time()
    # # # boxplot()
    # # # # get_best()
    # best_fitnesses_barplot()
    # # # # table_best()
