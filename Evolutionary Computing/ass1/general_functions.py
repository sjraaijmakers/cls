import pickle

def save_pickle(data, filename, enemy, mutpb, cxpb, N_SIMS, N_POP, N_GEN, path="plot_data/"):
    filename = path + filename + "_e_" + str(enemy) + "_m_" + str(mutpb) + "_c_" + str(cxpb) + "_s_" + str(N_SIMS) + "_p_" + str(N_POP) + "_g_" + str(N_GEN)  

    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)