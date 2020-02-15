import mandelbrot
import numpy as np
from tinydb import TinyDB, Query
from pickles import save_pickle


LIMITS = np.array([[-2.0, 2.0], [-2.0, 2.0]])


def insert_into_db(db, N_samples, N_iter, limits, N_hits, alg_type):
    db.insert({
        "N_samples": N_samples,
        "N_iterations": N_iter,
        "limits": limits.tolist(),
        "N_hits": N_hits,
        "alg_type": alg_type
    })    


# Function of number of iterations (assignment)
def get_i(N_samples, N_iter_range, alg_type, reps=20):
    db = TinyDB("data/db_i_100.json")

    print("ALG TYPE: " + str(alg_type) + " for " + str(reps) + " reps")

    for N_iter in N_iter_range:
        for _ in range(reps):
            if alg_type == "mc":
                points = mandelbrot.mc(N_samples, N_iter, LIMITS)
            elif alg_type == "lhs":
                points = mandelbrot.lhs(N_samples, N_iter, LIMITS)
            elif alg_type == "sbl":
                points = mandelbrot.sobol(N_samples, N_iter, LIMITS)

            insert_into_db(db, N_samples, int(N_iter), LIMITS, points.size, alg_type)
            
        print("Finished " + alg_type + " (N_samples=" + str(N_samples) + ", N_iter=" + str(N_iter) + ", reps=" + str(reps) + ")")

    print("Finished calculating all areas for " + str(alg_type) + ".")


# Function of number of samples
def get_s(N_samples_range, N_iter, alg_type, reps=20):
    db = TinyDB("data/db_s.json")    

    print("ALG TYPE: " + str(alg_type) + " for " + str(reps) + " reps")

    print("Started calculating areas from 0 to base_iter...")

    for N_samples in N_samples_range:
        for _ in range(reps):

            if alg_type == "mc":
                points = mandelbrot.mc(N_samples, N_iter, LIMITS)
            elif alg_type == "lhs":
                points = mandelbrot.lhs(N_samples, N_iter, LIMITS)
            elif alg_type == "sbl":
                points = mandelbrot.sobol(N_samples, N_iter, LIMITS)

            insert_into_db(db, int(N_samples), N_iter, LIMITS, points.size, alg_type)

        print("Finished " + alg_type + " (N_samples=" + str(N_samples) + ", N_iter=" + str(N_iter) + ", reps=" + str(reps) + ")")

    print("Finished calculating all areas for " + str(alg_type) + ".")


def clt(N_samples, N_iter, reps, alg_type):
    sizes = []
    
    for r in range(reps):
        if r % 10000 == 0:
            print(r)
        if alg_type == "mc":
            points = mandelbrot.mc(N_samples, LIMITS, N_iter)

        sizes.append(points.size)

    save_pickle(sizes, "data/clt")

    # db = TinyDB("data/db_clt.json")
    # for size in sizes:
    #     insert_into_db(db, N_samples, N_iter, LIMITS, size, alg_type)


if __name__ == '__main__':
    # #  I
    # stepsize = 100
    # base_iter = 10000
    # js = np.logspace(1, 4, 100)
    # get_i(10, js, "mc", 20)
    # get_i(10, js, "lhs", 20)
    # get_i(10, js, "sbl", 20)

    # S
    # stepsize = 100
    # ss = np.arange(1000, 10000 + stepsize, stepsize)
    # ss = np.logspace(1, 4, 100, dtype=int)
    # get_s(ss, 1000, "mc", 20)
    # get_s(ss, 1000, "lhs", 20)
    # get_s(ss, 1000, "sbl", 20)

    # clt(10, 1000, 1000*10000, "mc")
