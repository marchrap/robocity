from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
from animate_robots import animate_robots
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import time

routing_modes = ["random",
                 "random_multiple",
                 "hungarian",
                 "linear_separate_tasks",
                 "linear_joined_tasks",
                 "tsm",
                 "home"
                 ]

robot_types = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

if __name__ == "__main__":

    number_of_graphs = len(routing_modes)

    for routing_mode in routing_modes:

        robots = []

        world = World()

        for i in range(10):
            robot = Robot((0, 0), i, robot_type=robot_types[i])
            robot._start_node = np.random.choice(world.warehouses)
            robots.append(robot)

        if routing_mode == "random_multiple":
            assignment_cost = route_multiple(world, robots, mode="random", number_of_runs=1)
        else:
            assignment_cost = route(world, robots, mode=routing_mode)[1]

        fig