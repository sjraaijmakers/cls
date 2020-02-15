import pickle
import os.path
import numpy as np


def save_pickle(data, filename):
    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def open_pickle(filename):
    with open(filename + '.pickle', 'rb') as handle:
        return pickle.load(handle)


# def save_fittest(data):
#     with open('data/fittest_of_all_time.pickle', 'wb+') as handle:
#         pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     np.save('data/fittest_of_all_time', data[0]) # also dump the individual as a numpy array

# def get_fittest_numpy():
#     if os.path.isfile('data/fittest_of_all_time.npy'):
#         return np.load('data/fittest_of_all_time.npy')

# def get_fittest():
#     if os.path.isfile('data/fittest_of_all_time.pickle'):
#         with open('data/fittest_of_all_time.pickle', 'rb') as handle:
#             return pickle.load(handle)
#     else:
#         save_fittest([[], -300, None, None])
#         return get_fittest()