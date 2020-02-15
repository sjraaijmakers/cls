from os import listdir
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

sns.set(font_scale=2, rc={'figure.figsize':(10,10)})

def average(l):
    llen = len(l)
    def divide(x): return x / llen
    return list(map(divide, map(sum, zip(*l))))

def get_max_value(fitnesses):
    maxes = []
    indices = []

    for f in fitnesses:
        maxes.append(max(f))
        indices.append(f.index(max(f)))

    return indices[maxes.index(max(maxes))], max(maxes)

def open_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

def plot_data_set_paramtuning(stats, filename, fig, ax, filename_start):
    n_pop = 30
    n_sims = len(stats["avg"])

    # set tick for gens 0-10
    ax.set_xticks(np.arange(min(stats["gen"]), max(stats["gen"]) + 1, 1))

    # Split file name
    filename_s = filename.split("_")

    # crossover has a different splice array than nocx
    if(filename_start == "NN_crosover"):
        file_name_rec = "mupb: " + filename_s[6] + " cross_p: " + filename_s[8]
    else:
        file_name_rec = "mupb: " + filename_s[9] + " cross_p: " + filename_s[11]
        # try:
        #     if(average(stats["avg"])[8] > -73):
        #             print(file_name_rec, end=" final avg fitness: ")
        #             print(average(stats["avg"])[8])
        # except:
        #     print(average(stats["avg"]))

    # Plot average of all runs
    ax.plot(average(stats["avg"]))
    plt.xlabel("Generation")
    plt.ylabel("Avg. fitness")
    return fig, ax

def plot_NN_paramtuning(directory, filename_start):
    fig, ax = plt.subplots(figsize=(10,10))
    for f in listdir(directory):
        if f.startswith(filename_start):
            stats = open_pickle(directory+f)
            fig, ax = plot_data_set_paramtuning(stats, directory+f, fig, ax, filename_start)

    fig.tight_layout()
    plt.figure(figsize=(10,1))
    plt.ylim(-100, 100)

    plt.savefig("plots/" + filename_start + "_param_tuning" + ".pdf")


"""
No crossover plots
"""
def plot_no_cx_no_sel():
    fig, ax = plt.subplots(figsize=(10,10))
    n_pop = 100
    gen = 31

    for string_split, line_name in zip(["_e_2",  "_e_3",  "_e_4",], ["Enemy 2", "Enemy 3", "Enemy 4"]):

        stats = []
        directory = "plot_data/no_cx_no_sel/"

        for f in listdir(directory):
            if string_split in f:
                stat = (open_pickle(directory+f))
                stats.append(stat['avg'][0])
        plt.errorbar(np.arange(gen), np.mean(stats, axis=0), yerr=np.std(stats, axis=0), label="no cx", alpha=0.6)
            
    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.legend()
    plt.ylim(-100, 100)
    # plt.title("EA no cx, no selection " + line_name)
    plt.savefig("plots/avg_sd_no_cx_no_sel" + ".pdf")

def plot_avg_sd(string_split, line_name):
    fig, ax = plt.subplots(figsize=(10,8))
    n_pop = 100
    gen = 31

    """
    No crossover plots
    """
    stats = []
    directory = "plot_data/no_cx/"

    for f in listdir(directory):
        if string_split in f:
            stat = (open_pickle(directory+f))
            stats.append(stat['avg'][0])
            
    ax.errorbar(np.arange(gen), np.mean(stats, axis=0), yerr=np.std(stats, axis=0), label="no cx", alpha=0.6)
    fig.tight_layout()        

    """
    Crossover plots
    """
    stats = []
    directory = "plot_data/cx/"
    if(string_split == "_e_2"): #the 10 sequential runs data case
        f = "plot_data/cx/NN_crosover_l_2_m_0.1_c_0.9_s_10_p_100_g_30.pickle"
        stats = open_pickle(f)
        ax.errorbar(stats["gen"], np.mean(stats["avg"], axis=0), yerr=np.std(stats["avg"], axis=0), label="cx", alpha=0.6)
    else:
        for f in listdir(directory):
            if string_split in f:
                stat = (open_pickle(directory+f))
                stats.append(stat['avg'][0])
        ax.errorbar(np.arange(gen), np.mean(stats, axis=0), yerr=np.std(stats, axis=0), label="cx", alpha=0.6)

    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.legend()
    plt.ylim(-100, 100)
    # plt.title("EA's cx vs no cx, " + line_name)
    fig.tight_layout()        

    fig.tight_layout()        

    plt.savefig("plots/avg_sd" + string_split + ".pdf")

def box_plot():
    fig, ax = plt.subplots(figsize=(10,8))
    # Create empty dataframe
    df_all = pd.DataFrame(columns=["max", "enemy", "alg"])

    # Extend dataframe with AlG1
    for enemy in [2, 3, 4]:
        filename = "plot_data/merged_pickles/NN_nocx_enemy_" + str(enemy) + "_mut_0.1_cx_0.0_pop_100"
        stats = open_pickle(filename)
        df = pd.DataFrame()
        df["max"] = np.max(stats["avg"], axis=1)
        df["enemy"] = enemy
        df["alg"] = "nocx"
        df_all = pd.concat([df_all, df])

    # Extend dataframe with ALG2

    for enemy in [2, 3, 4]:
        filename = "plot_data/merged_pickles/NN_cx_enemy_" + str(enemy) + "_mut_0.1_cx_0.9_pop_100"
        stats = open_pickle(filename)
        df = pd.DataFrame()
        df["max"] = np.max(stats["avg"], axis=1)
        df["enemy"] = enemy
        df["alg"] = "cx"
        df_all = pd.concat([df_all, df])

    # Plot and change axis names    
    ax = sns.boxplot(x="enemy", y="max", hue="alg", data=df_all)
    plt.ylim(-100, 100)
    ax.set(xlabel='enemy', ylabel='fitness')
    fig.tight_layout()  
    plt.savefig("plots/boxplot.pdf")

def main():
    # # Param tuning plots
    # plot_NN_paramtuning("plot_data/param_tuning/", "NN_crosover") # small spelling mistake in datasets names, oops.
    # plot_NN_paramtuning("plot_data/param_tuning/", "NN_nocx")

    # # Plots for avg and sd
    # plot_avg_sd("_e_2", "Enemy 2")
    # plot_avg_sd("_e_3", "Enemy 3")
    # plot_avg_sd("_e_4", "Enemy 4")

    # # Plot for no cx and no selection
    # plot_no_cx_no_sel()

    box_plot()


if __name__ == "__main__":
    main()
