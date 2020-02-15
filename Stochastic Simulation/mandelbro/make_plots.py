import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tinydb import TinyDB, Query
import pandas as pd
from pickles import open_pickle


sns.set()


palette ={
    "mc":"C0",
    "lhs":"C1",
    "sbl":"C2"
}


def error_max_min(x):
    return abs(np.max(x) - np.min(x))


def error95(x):
    return (1.96 * np.std(x)) / np.sqrt(len(x))


def get_area(x):
    return (x[0][1] - x[0][0]) * (x[1][1] - x[1][0])
    

# asked for in the assignment
def plot_i(N_samples, save=False):
    # load runs
    db = TinyDB("data/db_i.json")
    df = pd.DataFrame(db)

    # get area of domain using "limits"
    df["domain_area"] = df["limits"].apply(get_area)

    # determine estimated area
    df["area"] = (df["N_hits"] / df["N_samples"]) * df["domain_area"]   

    heads = {}

    for alg_type in df["alg_type"].unique():
        head = df[(df["alg_type"] == alg_type) & (df["N_iterations"] == df["N_iterations"].max())]
        heads[alg_type] = np.mean(head["area"])

    df["error"] = abs(df["area"] - df["alg_type"].map(heads))

    df = df[df["N_samples"] == N_samples]

    mc_lhs = df[df["alg_type"] != "sbl"]
    mc_sbl = df[df["alg_type"] != "lhs"]

    # plot
    ax = sns.lineplot(x="N_iterations", y="error", hue="alg_type", palette=palette, data=mc_lhs)
    ax.set(xlabel=r"$N_{iterations}$", ylabel="relative error")
    ax.set_xscale("log")
    plt.show()

    ax = sns.lineplot(x="N_iterations", y="error", hue="alg_type", palette=palette, data=mc_sbl)
    ax.set(xlabel=r"$N_{iterations}$", ylabel="relative error")
    ax.set_xscale("log")
    plt.show()


def plot_s(N_iterations, save=False):
    # load runs
    db = TinyDB("data/db_s.json")
    df = pd.DataFrame(db)
    
    # get area of domain using "limits"
    df["domain_area"] = df["limits"].apply(get_area)

    # determine estimated area
    df["area"] = (df["N_hits"] / df["N_samples"]) * df["domain_area"]   

    heads = {}

    for alg_type in df["alg_type"].unique():
        head = df[(df["alg_type"] == alg_type) & (df["N_samples"] == df["N_samples"].max())]
        heads[alg_type] = np.mean(head["area"])

    df["error"] = abs(df["area"] - df["alg_type"].map(heads))
    df = df[df["N_iterations"] == N_iterations]

    mc_lhs = df[df["alg_type"] != "sbl"]
    mc_sbl = df[df["alg_type"] != "lhs"]

    # plot
    ax = sns.lineplot(x="N_samples", y="error", hue="alg_type", palette=palette, data=mc_lhs)
    ax.set(xlabel=r"$N_{samples}$", ylabel="relative error")
    ax.set_xscale("log")
    plt.show()

    ax = sns.lineplot(x="N_samples", y="error", hue="alg_type", palette=palette, data=mc_sbl)
    ax.set(xlabel=r"$N_{samples}$", ylabel="relative error")
    ax.set_xscale("log")
    plt.show()


def clt():
    k = open_pickle("data/clt")

    vals = np.split((np.asarray(k) / 10) * 16, 1000)

    # Take distribution of one sample
    ax = sns.distplot((np.asarray(vals[0]) / 10) * 16, label="mc")
    ax = ax.set(xlabel="area", ylabel="frequency")
    plt.show()

    # Take mean of all samples
    ax = sns.distplot(np.mean(vals, axis=1), label="mc")
    ax = ax.set(xlabel="area", ylabel="frequency")
    plt.show()


if __name__ == '__main__':
    # clt()
    # plot_s(1000)
    # plot_i(10)
    plot_i(100)
    # plot_i(1000)
