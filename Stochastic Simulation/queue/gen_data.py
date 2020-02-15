import mXc
import pandas as pd
from pickles import save_pickle
import numpy as np


""" MASTER FUNCTION: runs experiment with its params as lists (iterations) """

# Produces less data points (note: different output)
def run_experiment(filename, lambdas, mu, cs, customers, service_types=["M"], schedulers=["FIFO"], reps=100, scales=[None], verbose=True):
    d_st = []
    d_cs = []
    d_lambdas = []
    d_mus = []
    d_schedulers = []
    d_customers = []
    d_means = []
    d_stds = []
    d_scales = []

    for service_type in service_types:
        for scheduler in schedulers:
            for mc in customers:
                for c in cs:
                    for lambd_o in lambdas:
                        for scale in scales:
                            lambd = lambd_o * c

                            tmp = []
                            for _ in range(reps):
                                data = mXc.run(lambd, mu, c, service_type, scheduler, max_customers=mc, scale=scale)
                                wait_time = list(np.array(data)[:,0])
                                service_time = list(np.array(data)[:,1])
                                tmp += wait_time

                            tmp = np.array(tmp)
                            d_scales.append(scale)
                            d_means.append(np.mean(tmp))
                            d_stds.append(np.std(tmp))

                            d_st.append(service_type)
                            d_cs.append(c)
                            d_lambdas.append(lambd)
                            d_mus.append(mu)
                            d_schedulers.append(scheduler)
                            d_customers.append(mc)

                            if verbose:
                                print("Finished M/" + str(service_type) +"/" + str(c) + "\t(" + str(scheduler) + ")\treps=" + str(reps) + "\tmax_customers=" + str(mc) + 
                                    "\tlambda=" + str(lambd) + "\tmu=" + str(mu) + "\trho=" + str(lambd/(c*mu)) + "\tscale=" + str(scale))

    dt = {
        "service_type": d_st,
        "c": d_cs,
        "lambda": d_lambdas,
        "mu": d_mus,
        "scheduler": d_schedulers,
        "customers": d_customers,
        "wait_time_mean": d_means,
        "wait_time_std": d_stds,
        "scale": d_scales
    }

    df = pd.DataFrame.from_dict(dt)
    save_pickle(df, "data/" + str(filename))


""" Experiments related to question 2 """

# Experiment runs MMC for different C and different lambdas --> rhos
def experiment_rhos():
    lambdas = np.linspace(0.1, 2.5, num=10)
    mu = 2.6
    cs = [1, 2, 4]
    customers = [10000]

    run_experiment("experiment_rhos", lambdas, mu, cs, customers)


# Experiment runs MMC for different C and different customers (stop condition) """
def experiment_customers():
    lambdas = [2.5]
    mu = 2.6
    cs = [1, 2, 4]
    customers = np.logspace(2, 4, 20, dtype=int)

    run_experiment("experiment_customers", lambdas, mu, cs, customers)


""" Experiments related to question 3 """

# Experiment runs MMC for different C, for different lambdas --> rho and different schedulers (FIFO & SJF)
def experiment_schedulers():
    lambdas = np.linspace(0.1, 2.5, num=10)
    mu = 2.6
    cs = [1, 2, 4]
    customers = [10000]
    schedulers = ["FIFO", "SJF"]

    run_experiment("experiment_schedulers", lambdas, mu, cs, customers, schedulers=schedulers)


""" Experiments related to question 4 """

def experiment_d():
    lambdas = [2.5]
    mu = 2.6
    cs = [1, 2, 4]
    customers = np.logspace(2, 4, 20, dtype=int)
    service_types = ["D"]

    run_experiment("experiment_d", lambdas, mu, cs, customers, service_types=service_types)


def experiment_l():
    lambdas = [2.5]
    mu = 2.6
    cs = [1, 2, 4]
    customers = [10000]
    scales = [1, 2, 3, 4, 5]
    service_types = ["L"]

    run_experiment("experiment_l", lambdas, mu, cs, customers, service_types=service_types, scales=scales)


if __name__ == "__main__":
    # experiment_rhos()
    # experiment_customers()
    # experiment_schedulers()
    # experiment_d()
    experiment_l()