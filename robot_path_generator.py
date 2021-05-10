from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
from animate_robots import animate_robots, progress_bar, progress_bar2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import time

routing_mode = "home"
robot_types = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
timestr = time.strftime("%Y%m%d-%H%M%S")

if __name__ == "__main__":
    robots = []
    world = World(max_demand=30)

    for i in range(10):
        robot = Robot(np.array([0, 0]), i, robot_type=robot_types[i])
        robot._start_node = np.random.choice(world.warehouses)
        robots.append(robot)

    print("\n\t Routing robots with {}...".format(routing_mode))
    timer_start = time.time()
    assignment_cost = route(world, robots, mode=routing_mode)[1]
    computation_time = time.time() - timer_start

    filehandle = open('robot_path{}.txt'.format(timestr), 'w')
    filehandle.write("mode:\t{}\tassignment_cost:\t{}\tcomputation_time:\t{}\t\n".format(routing_mode, assignment_cost,
                                                                                         computation_time))
    for robot in robots:
        for node in robot.node_path:
            filehandle.write("{}\t".format(node))
        filehandle.write("\n")
