import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pickles import open_pickle


sns.set(font_scale=1.5)


palette ={
    1: "r",
    2: "g",
    4: "b"
}


def calc_pi_w(c, rho):
    fp = ((c * rho)**c) / np.math.factorial(c)
    summ = 0
    for n in range(0, c-1):
        summ  = ((c * rho)**n) / np.math.factorial(n)

    sp_in = ((1-rho) * summ + (((c * rho)**c)/ np.math.factorial(c)))**(-1)
    return fp * sp_in


def mean_wait_n(c, mu, lambd, D=1):
    rho = lambd / (c * mu)
    pi_w = calc_pi_w(c, rho)
    return (pi_w * (1/(D*(1-rho))) * (1/(c * mu)))


def get_stds(df, hue, x, ax):
    for c in df[hue].unique():
        df_tmp = df[df[hue] == c]
        # ax.errorbar(df_tmp[x], df_tmp["wait_time_mean"], yerr=df_tmp["wait_time_std"], ecolor=palette[c], alpha=0.2)
        ax.fill_between(df_tmp[x], y1=df_tmp["wait_time_mean"] - df_tmp["wait_time_std"], y2=df_tmp["wait_time_mean"] + df_tmp["wait_time_std"], alpha=0.2, facecolor=palette[c])


""" Plots related to question 2 """


def plot_experiment_rhos(save=False):
    df = open_pickle("data/experiment_schedulers")
    df["rho"] = df["lambda"] / (df["c"] * df["mu"])
    df = df[df["scheduler"] == "FIFO"]      
    
    ax = sns.lineplot(x="rho", y="wait_time_mean", hue="c", data=df, palette=palette)

    get_stds(df, "c", "rho", ax)

    ax.set(xlabel=r"$\rho$", ylabel=r"$\bar{W}_{empirical}$")
    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_rhos.pdf")
    else:
        plt.show()

    plt.clf()


# This is Marcus' plot
def plot_experiment_customers_marcus(save=False):
    df = open_pickle("data/experiment_customers")
    df["rho"] = df["lambda"] / (df["c"] * df["mu"])

    lambd = df["lambda"].unique()
    c = df["c"].unique()
    mu = df["mu"].unique()[0]

    mean_wait_time_1 = mean_wait_n(c[0], mu, lambd[0])
    mean_wait_time_2 = mean_wait_n(c[1], mu, lambd[1])
    mean_wait_time_4 = mean_wait_n(c[2], mu, lambd[2])

    ax = sns.lineplot(x="customers", y="wait_time_mean", hue="c", data=df, palette=palette)
    ax.set(xlabel=r"$N_{customers}$", ylabel=r"waiting time")
    ax.set_xscale("log")

    ax.axhline(mean_wait_time_1, color="r", linestyle="dashdot", alpha=1.0)
    ax.axhline(mean_wait_time_2, color="g", linestyle="dashdot", alpha=1.0)
    ax.axhline(mean_wait_time_4, color="b", linestyle="dashdot", alpha=1.0)

    get_stds(df, "c", "customers", ax)
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_customers_marcus.pdf")
    else:
        plt.show()

    plt.clf()


# Just plot the error instead
def plot_experiment_customers_error(save=False):
    df = open_pickle("data/experiment_customers")

    lambd = df["lambda"].unique()
    c = df["c"].unique()
    mu = df["mu"].unique()[0]

    mean_wait_time_1 = mean_wait_n(c[0], mu, lambd[0])
    mean_wait_time_2 = mean_wait_n(c[1], mu, lambd[1])
    mean_wait_time_4 = mean_wait_n(c[2], mu, lambd[2])

    dc = {
        1: mean_wait_time_1,
        2: mean_wait_time_2,
        4: mean_wait_time_4
    }

    df["wq"] = df["c"].map(dc)
    df["error"] = df["wq"] - df["wait_time_mean"]

    ax = sns.lineplot(x="customers", y="error", hue="c", data=df, palette=palette)
    ax.set(xlabel=r"$N_{customers}$", ylabel=r"$|E(W) - \bar{W}_{empirical}|$")
    ax.set_xscale("log")

    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_customers_error.pdf")
    else:
        plt.show()

    plt.clf()


""" Plots related to question 3 """

def plot_experiment_schedulers(save=False):
    df = open_pickle("data/experiment_schedulers")
    df = df[df["scheduler"] == "SJF"]
    df["rho"] = df["lambda"] / (df["c"] * df["mu"])

    ax = sns.lineplot(x="rho", y="wait_time_mean", hue="c", palette=palette, data=df)
    ax.set(xlabel=r"$\rho$", ylabel=r"$\bar{W}_{empirical}$")
    
    get_stds(df, "c", "rho", ax)

    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_schedulers.pdf")
    else:
        plt.show()

    plt.clf()


""" Plots related to question 4 """


def plot_experiment_d(save=False):
    df = open_pickle("data/experiment_d")
    df["rho"] = df["lambda"] / (df["c"] * df["mu"])

    df = df[df["service_type"] == "D"]

    lambd = df["lambda"].unique()
    c = df["c"].unique()
    mu = df["mu"].unique()[0]

    mean_wait_time_1 = mean_wait_n(c[0], mu, lambd[0], D=2)
    mean_wait_time_2 = mean_wait_n(c[1], mu, lambd[1], D=2)
    mean_wait_time_4 = mean_wait_n(c[2], mu, lambd[2], D=2)
    
    ax = sns.lineplot(x="customers", y="wait_time_mean", hue="c", palette=palette, data=df)
    ax.set(xlabel=r"$N_{customers}$", ylabel="waiting time")
    ax.set_xscale("log")

    ax.axhline(mean_wait_time_1, color="r", linestyle="dashdot", alpha=1.0)
    ax.axhline(mean_wait_time_2, color="g", linestyle="dashdot", alpha=1.0)
    ax.axhline(mean_wait_time_4, color="b", linestyle="dashdot", alpha=1.0)

    get_stds(df, "c", "customers", ax)
  
    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_d.pdf")
    else:
        plt.show()
    
    plt.clf()

# Just plot the error instead
def plot_experiment_d_error(save=False):
    df = open_pickle("data/experiment_d")

    lambd = df["lambda"].unique()
    c = df["c"].unique()
    mu = df["mu"].unique()[0]

    mean_wait_time_1 = mean_wait_n(c[0], mu, lambd[0], D=2)
    mean_wait_time_2 = mean_wait_n(c[1], mu, lambd[1], D=2)
    mean_wait_time_4 = mean_wait_n(c[2], mu, lambd[2], D=2)

    dc = {
        1: mean_wait_time_1,
        2: mean_wait_time_2,
        4: mean_wait_time_4
    }

    df["wq"] = df["c"].map(dc)
    df["error"] = df["wq"] - df["wait_time_mean"]

    ax = sns.lineplot(x="customers", y="error", hue="c", data=df, palette=palette)
    ax.set(xlabel=r"$N_{customers}$", ylabel=r"$|E(W) - \bar{W}_{empirical}|$")
    ax.set_xscale("log")

    plt.legend()
    plt.tight_layout()

    if save:
        plt.savefig("figs/plot_experiment_d_error.pdf")
    else:
        plt.show()

    plt.clf()


# Just plot the error instead
def plot_experiment_l(save=False):
    df = open_pickle("data/experiment_l")

    ax = sns.lineplot(x="scale", y="wait_time_mean", hue="c", data=df, palette=palette)
    ax.set(xlabel=r"$\theta$", ylabel=r"$\bar{W}_{empirical}$")

    plt.legend()
    plt.tight_layout()

    get_stds(df, "c", "scale", ax)

    if save:
        plt.savefig("figs/plot_experiment_l.pdf")
    else:
        plt.show()

    plt.clf()


if __name__ == "__main__":
    # plot_experiment_rhos(True)
    # plot_experiment_customers_marcus(True)
    # plot_experiment_customers_error(True)
    # plot_experiment_schedulers()
    # plot_experiment_d(True)
    # plot_experiment_d_error(True)
    plot_experiment_l(True)
    