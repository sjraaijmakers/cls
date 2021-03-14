import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from network import Network
import pandas as pd
from sa import SA
from circle import Circle
from pickles import open_pickle


palette ={
    100: "c",
    200: "m",
    300: "r",
    400: "g",
    500: "b",
    700: "y",
    1000: "k"
}


# For different cooling schedules plot the temp
def plot_TSP_cs_temp(filename, save=False):
    df = open_pickle("data/" + filename + "_cooling_schedules")
    ax = sns.lineplot(x="n", y="temp", hue="cooling_schedule", ci=None, data=df)

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_cs_temp_lin.pdf")
    else:
        plt.show()
    plt.clf()    


# For different cooling schedules plot the cost
def plot_TSP_cs_weight(filename, save=False):
    df = open_pickle("data/" + filename + "_cooling_schedules")

    optimal_solution_weight = Network("routes/" + filename).optimal_solution_weight

    ax = sns.lineplot(x="n", y="cost", hue="cooling_schedule", data=df)
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_cooling_schedule_cost.pdf")
    else:
        plt.show()
        
    plt.clf()    
    

# For different T0 plot the temps
def plot_TSP_temp_temps(filename, save=False):
    df = open_pickle("data/" + filename + "_temps")

    sns.lineplot(x="n", y="temp", hue="init_temp", ci=None, data=df, palette=sns.color_palette('husl', n_colors=3))

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_temp_temps.pdf")
    else:
        plt.show()
    plt.clf()    
    

# For different T0 plot the cost
def plot_TSP_temp_cost(filename, save=False):
    df = open_pickle("data/" + filename + "_temps")

    optimal_solution_weight = Network("routes/" + filename).optimal_solution_weight

    ax = sns.lineplot(x="n", y="cost", hue="init_temp", data=df, palette=sns.color_palette('husl', n_colors=3))
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_temp_cost.pdf")
    else:
        plt.show()
    plt.clf()    
    

# For different MCL plot the cost
def plot_TSP_mcl(filename, save=False):
    df = open_pickle("data/" + filename + "_mcls")

    optimal_solution_weight = Network("routes/" + filename).optimal_solution_weight

    ax = sns.lineplot(x="n", y="cost", hue="l", data=df, palette=palette)
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_mcls.pdf")
    else:
        plt.show()
    plt.clf()    


# Marcus plot
def plot_CIR_cs_weight(filename, save=False):
    df = open_pickle("data/" + filename + "_cooling_schedules")

    optimal_solution_weight = 9.985281 # From https://www.nrcresearchpress.com/doi/pdf/10.1139/v88-343

    ax = sns.lineplot(x="n", y="cost", hue="cooling_schedule", data=df)
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)
    ax.set(xlabel="n", ylabel="E")

    plt.tight_layout()
    if save:
        plt.savefig("figs/" + filename + "_cooling_schedule_cost.pdf")
    else:
        plt.show()
    
    plt.clf() 


def plot_CIR_mcl(filename, save=False):
    df = open_pickle("data/" + filename + "_mcls")

    optimal_solution_weight = 9.985281

    ax = sns.lineplot(x="n", y="cost", hue="l", data=df, palette=palette)
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)
    ax.set(xlabel="n", ylabel="E")

    plt.tight_layout()

    if save:
        plt.savefig("figs/" + filename + "mcl" + ".pdf")
        plt.ylim(0, 100)
        plt.xlim(500,1000)
        plt.savefig("figs/" + filename + "mcl_zoomed" + ".pdf")
    else:
        plt.show()
    

def plot_CIR_edit_types(filename1, filename2, save=False):
    # Open the two dataframes
    df_1 = open_pickle("data/" + filename1)
    df_2 = open_pickle("data/" + filename2)

    #  Add the edit type to the dataframes
    e_type_pf = []
    e_type_pp = []
    for _ in range(0, df_1.shape[0]):
        e_type_pf.append("pertubate_force")
        e_type_pp.append("pertubate_points")

    df_1.insert(1, "edit_type", e_type_pf, True) 
    df_2.insert(1, "edit_type", e_type_pp, True) 

    df = [df_1, df_2]
    df = pd.concat(df)

    optimal_solution_weight = 9.985281

    ax = sns.lineplot(x="n", y="cost", hue="edit_type", data=df)
    ax.axhline(optimal_solution_weight, color="black", linestyle="dashed", alpha=0.8)
    ax.set(xlabel="n", ylabel="E")

    plt.tight_layout()

    if save:
        plt.savefig("figs/" + filename1 + "_"  + filename2 + ".pdf")
    else:
        plt.show()


if __name__ == "__main__":
    """ TSP experiments """
    # plot_TSP_cs_temp("a280", True)
    # plot_TSP_cs_weight("a280", True)
    # plot_TSP_temp_temps("a280", True)
    # plot_TSP_temp_cost("a280", True)
    # plot_TSP_mcl("a280", True)

    """ Circle experiments """

    # plot_CIR_cs_weight("circle_6", True)
    # plot_CIR_mcl("circle_6", True)
    # plot_CIR_edit_types("circle_6_edit_type_pertubate_force", "circle_6_edit_type_pertubate_points", save=True)
