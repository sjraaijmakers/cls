from network import Network
import numpy as np
import sys
from circle import Circle
import circle


class SA:
    def __init__(self, network, initial=None):
        self.network = network

        if initial:
            self.initial = initial
        else:
            self.initial = self.network.get_initial()

        self.solutions = []
        self.costs = []
        self.temps = []
        self.ns = []

    def edit(self, solution, edit_type):
        candidate = solution.copy()

        # 2-opt of list
        if edit_type == "2-opt":
            l = np.random.randint(2, len(solution) - 1)
            i = np.random.randint(0, len(solution) - l)
            candidate[i: (i + l)] = reversed(candidate[i: (i + l)])
        elif edit_type == "random_gen":
            for point in candidate:
                point[0], point[1] = circle.random_gen()
        elif edit_type == "pertubate_points":
            for point in candidate:
                point[0], point[1] = circle.pertubate_points(point[0], point[1])
        elif edit_type == "pertubate_force":
            for x in range(len(candidate)):
                candidate[x][0], candidate[x][1] = circle.pertubate_with_force_vector_point(x, candidate)

        return candidate


    # Acceptance probability according to SA
    def p_acceptance(self, temp, current_weight, candidate_weight):
        return np.exp(-abs(candidate_weight - current_weight) / temp)


    def should_accept(self, temp, current_weight, candidate_weight):
        return np.random.uniform(0, 1) < self.p_acceptance(temp, current_weight, candidate_weight)


    # push values to list which will be returned
    def push(self, candidate, temp, n):
        candidate_weight = self.network.get_weight(candidate)

        self.solutions.append(candidate)
        self.costs.append(candidate_weight)
        self.temps.append(temp)
        self.ns.append(n)


    # reset push lists
    def reset_lists(self):
        self.costs = []
        self.solutions = []
        self.temps = []
        self.ns = []


    # run simulation anealing with params
    def run(self, temp, alpha, edit_type, n, l, cooling_schedule="exponential", verbose=False):
        self.reset_lists()

        current = self.initial.copy()

        self.push(current, temp, -1)

        t_0 = temp

        # Generate n markov chains...
        for i in range(n):
            # ...of length l
            for j in range(l):
                # create candidate
                candidate = self.edit(current, edit_type)
                candidate_weight = self.network.get_weight(candidate)
                current_weight = self.network.get_weight(current)

                accepted = current

                if candidate_weight < current_weight or self.should_accept(temp, current_weight, candidate_weight):
                    accepted = candidate

                current = accepted

            self.push(accepted, temp, i)

            if cooling_schedule == "exponential":
                temp *= alpha
            elif cooling_schedule == "linear":
                B = (t_0 - (t_0 * (alpha ** n))) / n
                temp -= B
            else:
                raise Exception("Unknown cooling schedule")

        return self.ns, self.costs, self.temps, self.solutions
