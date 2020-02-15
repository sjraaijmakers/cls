import pickle


def save_pickle(data, filename):
    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def open_pickle(filename):
    with open(filename + '.pickle', 'rb') as handle:
        return pickle.load(handle)
