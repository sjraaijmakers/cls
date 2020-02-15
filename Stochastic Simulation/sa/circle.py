import numpy as np
import matplotlib.pyplot as plt

"""
https://www.nrcresearchpress.com/doi/pdf/10.1139/v88-343
"""

class Circle:
    def __init__(self, N):
        self.N = N
        self.name = "circle_" + str(N)

    def get_initial(self, init_type="random"):
        np.random.seed(420)
        if init_type == "random":
            points = self.gen_points(self.N)
            np.random.seed(None)
            return points

    def gen_points(self, N):
        points = []
        for _ in range(N):
            x, y = random_gen()
            points.append([x, y])
        return np.asarray(points)

    def get_weight(self, points):
        total_energy = 0
        for i in range(0, len(points)):
            # total_energy += 1/np.linalg.norm(points - r_i)
            for j in range(0, len(points)):
                if i != j:
                    r_i = points[i]
                    r_j = points[j]

                    total_energy += 1/np.linalg.norm(r_i - r_j)
        return 0.5 * total_energy

def random_gen():
    t = 2 * np.pi * np.random.uniform()
    r = np.sqrt(np.random.uniform())
    x = r * np.cos(t)
    y = r * np.sin(t)
    return x, y

def decrement_point(val):
    if val > 0:
        return val - 10**(-2)
    return val + 10**(-2)

def normify(vec):
    vec = np.asarray(vec)
    vec = vec/np.linalg.norm(vec)
    return vec

def boundary(x, y, wrap=True):
    if np.sqrt((x)**2 + (y)**2) > 1:
        # Boundary wrapping of the points
        if wrap:
            x = -1 * x
            y = -1 * y
        vec = normify([x, y]) # bring back into circle
        return vec[0], vec[1]
    return x, y

def pertubate_points(x, y):
    if np.random.uniform() < 0.5:
        x += np.random.uniform(0.01, 10**(-6))
    else:
        x -= np.random.uniform(0.01, 10**(-6))

    if np.random.uniform() < 0.5:
        y += np.random.uniform(0.01, 10**(-6))
    else:
        y -= np.random.uniform(0.01, 10**(-6))

    return boundary(x, y)

def calc_force_between_points(point_from, point_to):
    diff = point_from - point_to
    return diff/np.linalg.norm(diff, ord=3) # vary the order here?

def pertubate_with_force_vector_point(i, points):
    current_p = points[i]

    directions = []
    for j in range(len(points)):
        if j != i:
            directions.append(calc_force_between_points(current_p, points[j]))

    directions = np.asarray(directions)
    total_force_vector = np.sum(directions, axis=0)
    total_force_vector = normify(total_force_vector)

    scale = 0.01
    x, y = boundary(current_p[0] + scale * total_force_vector[0], current_p[1] + scale * total_force_vector[1], wrap=False)

    return x, y