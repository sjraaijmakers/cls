import simpy
import random
import numpy as np
from time import sleep


class Servers(object):
    def __init__(self, env, mu, c, scheduler):
        self.env = env
        # Start the run process everytime an instance is created.
        self.c = c
        self.handled = 0

        if scheduler == "FIFO":
            self.server = simpy.Resource(env, self.c)
        elif scheduler == "SJF":
            self.server = simpy.PriorityResource(env, self.c)
        else:
            raise Exception("Unknown scheduler type.")


    def service(self, client_service_time):
        yield self.env.timeout(client_service_time)
        self.handled += 1


def client(env, client_id, servers, mu, scheduler, data, service_type, scale=None):
    service_time = None
    if service_type == "D":
        service_time = 1/mu 
    elif service_type == "L":
        if np.random.uniform(0, 1) < 0.75:
            service_time = np.random.exponential(1/mu)
        else:
            service_time = np.random.exponential((1/mu)*scale)
    elif service_type == "M":
        service_time = np.random.exponential(1/mu)
    else:
        raise Exception("Unknown service type.")

    wait_time_start = env.now

    f = None
    if scheduler == "FIFO":
        f = servers.server.request()
    elif scheduler == "SJF":
        f = servers.server.request(priority=service_time)
        if service_type == "D":
            raise Exception ("MDC does not support SJF.")
    else:
        raise Exception("Unknown scheduler type.")

    with f as request:
        yield request

        handle_start = env.now

        yield env.process(servers.service(service_time))

        handle_end = env.now
        # print(client_id, " done at ", handle_end)

        data.append([handle_start - wait_time_start, service_time])


def setup(env, lambd, mu, c, scheduler, data, service_type, max_customers, scale=None):
    # make environment, and servers
    servers = Servers(env, mu, c, scheduler)

    client_num = 0
    t = 0

    """
    Only generate max customers clients and all of these are handled and their data written to the dictionary.
    Queue congestion is held with this.
    """
    while client_num < max_customers:
        # Generate a poisson, new clients. They are queued FIFO if the "server" resource is not available
        next_client_arrival = random.expovariate(lambd) # at mean Lambda
        yield env.timeout(next_client_arrival)
        env.process(client(env, client_num, servers, mu, scheduler, data, service_type, scale))
        t += next_client_arrival
        client_num +=1

def run(lambd, mu, c, service_type, scheduler="FIFO", max_customers=100, scale=None):
    env = simpy.Environment()

    data = []

    env.process(setup(env, lambd, mu, c, scheduler, data, service_type, max_customers, scale))
    env.run()

    return data
