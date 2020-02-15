import numpy as np
import pickle


def open_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def save_pickle(data, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def merge_pickle(enemy, mut, cx):
    new_dic ={}
    avgs = []
    maxs = []

    # Set filename
    path = "plot_data"
    alg_type = "cx"

    s = 1
    pop = 100
    gen = 30
    
    for r in np.arange(10):
        filename = path + "/" + alg_type + "/NN_crosover_run_" + str(r) + "_e_" + str(enemy) + "_m_" + str(mut) + "_c_" + str(cx) + "_s_" + str(s) + "_p_" + str(pop) + "_g_" + str(gen) + ".pickle" 

        stats = open_pickle(filename)
        avgs.append(stats["avg"][0])
        maxs.append(stats["max"][0])
        
    sts = {
        "gen": stats["gen"],
        "avg": avgs,
        "max": maxs
    }

    # Save new dictionary to dir merged_pickles
    new_fn = path + "/merged_pickles/NN_" + alg_type + "_enemy_" +str(enemy) + "_mut_" + str(mut) + "_cx_" + str(cx) + "_pop_" + str(pop)
    save_pickle(sts, new_fn)


def main():
    # Choose "run" to merge
    merge_pickle(3, 0.1, 0.9)


if __name__ == "__main__":
    main()