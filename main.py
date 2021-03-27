from world import World
from robot_config import Robot
from routing_algorithm import routing_alorithm
from animate_robots import animate_robots

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

if __name__ == "__main__":
    # Run a test
    world = World()
    # world.plot()
    # print(list(nx.all_pairs_dijkstra(world.graph)))

    for node in world.graph.nodes:
        if world.graph.nodes[node]['type'] == 0:
            factory_pos = np.array(world.graph.nodes[node]['pos'])

    print(factory_pos)

    robots = []
    for i in range(10):
        robots.append(Robot(factory_pos, i))

    animate_robots(world, robots)