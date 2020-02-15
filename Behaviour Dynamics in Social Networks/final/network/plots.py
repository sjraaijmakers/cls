import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np


def ww1():
    return np.array([13, 20, 21, 22]) - 1, "hyperbolic_discounting"


def wsw():
    return np.array([1]) - 1, "stepmod"


def hebb():
    return np.array([4, 5, 18]) - 1, "hebb"


def base():
    return np.array([4, 5, 6, 7, 9, 10, 11, 12]) - 1, "base"


def tun():
    return np.array([5]) - 1, "tuning"


def fas():
    return np.array([13, 14, 15, 16, 17, 18, 19, 21]) - 1, "fas"


def alogistic(sigma, tau, yk):
    return (1 / (1 + np.exp(-sigma * (yk - tau))) - 1 / (1 + np.exp(sigma * tau))) * (1 + np.exp(-sigma * tau))

def plot_na():
    labels = [
        r'$ws_w$',
        r'$ss_w$',
        r'$srs_w$',
        r'$ps_{ai}$',
        r'$es_{ai}$',
        r'$cs_{ai}$',
        r'$vs_{ei}$',
        r'$dw_{s}$',
        r'$ws_{ei}$',
        r'$ss_{ei}$',
        r'$srs_{ei}$',
        r'$fs_{ei}$',
        r'W1',
        r'W2', 
        r'W3',
        r'W4',
        r'W5',
        r'W6',
        r'EC',
        r'UVC',
        r'WW1',
        r'TI'
    ]

    df = pd.read_csv('model_adaptive_3.csv', names=labels)
    
    dt = 1
    endtimeofsimulation = 200

    ts = np.arange(0, endtimeofsimulation+dt, dt)

    states, name = tun()

    plt.scatter([199], [0.5], color="red", label="emperical")

    for i in states:

        linestyle = "-"
        if i >= 12:
            linestyle = "-"
        
        plt.plot(ts, df.iloc[:,i], alpha=1, linestyle=linestyle, label=df.columns[i])

    plt.xlabel("Days")
    # plt.xlim(0, 50)
    plt.ylim(top=1)

    plt.ylabel("Intensity")    
    plt.legend()
    plt.tight_layout()
    plt.savefig("figs/" + name + "_3.png")
    plt.show()

    print(df.iloc[:,4])

if __name__ == "__main__":
    plot_na()