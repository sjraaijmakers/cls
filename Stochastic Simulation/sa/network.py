import numpy as np


class Network:
    def __init__(self, filename):
        self.filename = filename
        self.network = {}

        self.parse_network()
        self.distance_matrix = self.get_distance_matrix()

        self.optimal_solution = self.parse_optimal_solution()
        self.optimal_solution_weight = self.get_weight(self.optimal_solution)


    def parse_network(self):
        f = open(self.filename + ".tsp.txt", "r")

        for line in f:
            line = line.strip()
            # parse nodes & edges
            if(line[0].isdigit()):
                line = line.strip().split()
                node_number = int(line[0])
                node_x, node_y = line[1:]
                self.network[node_number] = Point(node_x, node_y)

            # parse context
            else:
                line = line.replace(' ','').strip().split(":")
                if len(line) > 1:
                    setattr(self, line[0].lower(), line[1])

    
    def parse_optimal_solution(self):
        f = open(self.filename + ".opt.tour.txt", "r")
        sol = []
        for line in f:
            line = line.strip()
            if(line[0].isdigit()):
                line = line.strip().split()
                sol.append(int(line[0]))
        return sol


    def get_initial(self, init_type="random", sol=None):
        np.random.seed(420)

        if init_type == "random":
            k = list(np.random.choice(len(self.network), len(self.network), replace=False) + 1)
            np.random.seed(None)
        elif sol:
            k = sol
        return k


    def get_distance_matrix(self):
        distance_matrix = np.empty([len(self.network) + 1, len(self.network) + 1])

        for k1, v1 in self.network.items():
            for k2, v2 in self.network.items():
                distance_matrix[k1][k2] = v1.get_distance(v2)

        return distance_matrix


    def get_weight(self, path):
        return sum([self.distance_matrix[i, j] for i, j in zip(path, path[1:] + [path[0]])])


class Point:
    def __init__(self, x, y, random=False):
        if random:
            self.x, self.y = self.random_gen()
        else:                
            self.x = int(x)
            self.y = int(y)
        

    def get_distance(self, node):
        x1, y1 = self.x, self.y
        x2, y2 = node.x, node.y
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    def random_gen(self):
        t = 2 * np.pi * np.random.uniform()
        r = np.sqrt(np.random.uniform())
        x = r * np.cos(t)
        y = r * np.sin(t)
        return x, y


    def __repr__(self):
        return str(self.x) + ", " + str(self.y)

