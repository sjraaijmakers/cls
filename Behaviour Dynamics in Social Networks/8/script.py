import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


sns.set()


def plot_1():
    df = pd.read_csv("new_empirical.xls")
    ax = sns.lineplot(data=df, legend=False)
    ax.set(xlabel="iterations", ylabel="RMSE")
    plt.savefig("rmse_empirical_all.pdf")


def plot_2(time_points, states, states_nums, filename):
    df = pd.read_csv("exp2.csv", names=[1,2,3,4,5,6,7,8,9,10,11,12])
    xs_all  = np.arange(0, 30.5, 0.5)
    
    for i, state in enumerate(states):
        plt.scatter(time_points, state, label="")
        plt.plot(xs_all, df[states_nums[i]], label=r"$X_{" + str(states_nums[i]) + "}$") 
        
    plt.xlim(0, 30)
    plt.xlabel("time")
    plt.legend()
    plt.savefig(filename)


if __name__ == "__main__":
    # time_points = [2, 5.9, 14.3, 21.1, 29.2]
    # state_1 = [0.90, 0.82, 0.72, 0.67, 0.63]
    # state_6 = [0.54, 0.52, 0.49, 0.47, 0.46]
    # state_12 = [0.03, 0.13, 0.24, 0.29, 0.33]
    # states = [state_1, state_6, state_12]
    # states_nums = [1, 6, 12]

    # time_points = [2, 5, 8, 11, 14, 17, 20, 23, 26, 30]
    # state_2 = [0.96, 0.89,  0.85, 0.82, 0.78, 0.76, 0.73, 0.71, 0.69, 0.67]
    # state_4 = [0.79, 0.76, 0.74, 0.73, 0.72, 0.71, 0.71, 0.7, 0.69, 0.68]
    # state_7 = [0.59, 0.67, 0.67, 0.67, 0.67, 0.66, 0.65, 0.66, 0.65, 0.65]
    # state_12 = [0.13, 0.26, 0.28, 0.29, 0.29, 0.3, 0.31, 0.32, 0.32, 0.33]
    # states = [state_2, state_4, state_7, state_12]
    # states_nums = [2, 4, 7, 12]

    # plot_2(time_points, states, states_nums, "plot_3.pdf")

    time_points = [3.1, 11.9, 20.2, 25.2, 28, 30]
    state_3 = [0.92, 0.85, 0.81, 0.79, 0.78, 0.77]
    state_5 = [0.75, 0.74, 0.73, 0.71, 0.71, 0.7]
    state_9 = [0.4, 0.55, 0.61, 0.64, 0.65, 0.65]
    state_10 = [0.25, 0.28, 0.3, 0.31, 0.32, 0.32]
    state_11 = [0.18, 0.32, 0.39, 0.41, 0.42, 0.43]
    states = [state_3, state_5, state_9, state_10, state_11]
    states_nums = [3, 5, 9, 10, 11]

    plot_2(time_points, states, states_nums, "plot_2.pdf")


