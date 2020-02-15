import numpy as np
from numba import njit, prange, jit
from smt.sampling_methods import LHS
import sobol_seq


def get_lhs_samples(N_samples, xlimits):
    sampling = LHS(xlimits=xlimits)
    samples = sampling(N_samples)
    return samples[:,0] + 1j * samples[:,1]


@njit
def is_point_in_mandelbrot(c, N_iter):
    """ c is in mandelbrot set if for all iterations c <= 2 """
    z = 0 + 0j
    for _ in range(N_iter):
        z = z ** 2 + c
        if abs(z.real) > 2 or abs(z.imag) > 2:
            return False
    return True


@njit(parallel=True)
def mc(N_samples, N_iter, limits):
    points = np.empty(N_samples, dtype=np.complex_)
    N_hits = 0

    for _ in prange(N_samples):
        c = complex(np.random.uniform(limits[0][0], limits[0][1]), np.random.uniform(limits[1][0], limits[1][1]))

        if is_point_in_mandelbrot(c, N_iter):
            points[N_hits] = c
            N_hits += 1

    return points[:N_hits]


def sobol(N_samples, N_iter, limits):
    p = sobol_seq.i4_sobol_generate(2, N_samples) # get sobol sequence

    U = np.random.rand(N_samples, 2) # vector U for randomizing
    Y = np.add(p, U)
    Y = np.mod(Y, 1) # mod by 1 to keep the values bound in 0..1

    sobol_points = (np.asarray(Y) * 4) - 2
    complex_samples = sobol_points[:,0] + 1j * sobol_points[:,1]

    points = np.empty(N_samples, dtype=np.complex_)
    N_hits = 0

    for i in range(complex_samples.size):
        c = complex_samples[i]

        if is_point_in_mandelbrot(c, N_iter):
            points[N_hits] = c
            N_hits += 1

    return points[:N_hits]


def lhs(N_samples, N_iter, limits):
    complex_samples = get_lhs_samples(N_samples, limits)

    points = np.empty(N_samples, dtype=np.complex_)
    N_hits = 0

    for i in range(complex_samples.size):
        c = complex_samples[i]

        if is_point_in_mandelbrot(c, N_iter):
            points[N_hits] = c
            N_hits += 1

    return points[:N_hits]
