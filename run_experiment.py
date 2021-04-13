from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
import numpy as np
import matplotlib as mpl
import time

import progressbar

number_of_robots = 10
number_of_runs_for_random = 25

results = {}

routing_modes = ["random",
                 "random_multiple",
                 "hungarian",
                 "linear_separate_tasks",
                 "linear_joined_tasks",
                 # "tsm",
                 # "home"
                 ]

robot_distributions = np.array([[number_of_robots, 0, 0]])

if __name__ == "__main__":

    for i in range(number_of_robots):
        robot_distributions = np.r_[robot_distributions, [[number_of_robots - i - 1, i+1, 0]]]

    print(robot_distributions)

    bar = progressbar.ProgressBar(max_value=number_of_robots * len(robot_distributions) * 2, redirect_stdout=True)
    itr = 1
    # bar = progressbar.

    # Open file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filehandle = open('results{}.txt'.format(timestr), 'w')
    filehandle.write('routing_mode\trobot_distribution\tassignment_cost\tcomputation_time\ttotal_speed_capacity\n')

    for routing_mode in routing_modes:
        for robot_distribution in robot_distributions:
            print("\n\t Running in", routing_mode, "routing mode with", number_of_robots, "robots in",
                  robot_distribution, "configuration")

            print("\n\t Initialising world...")
            bar.update(itr)
            itr += 1
            world = World(number_of_hospitals=15)

            # Initialize the robots in the warehouse
            robots = []
            print("\n\t World created. Assigning robots to warehouses...\n")

            # Distribute robot types
            robot_distribution = np.round(number_of_robots * robot_distribution / np.sum(robot_distribution))

            print("robot_distribution: ", robot_distribution)

            for i in range(number_of_robots):
                warehouse = np.random.choice(world.warehouses)
                pointer = world.graph.nodes[warehouse]
                position = np.array([pointer['x'], pointer['y']])

                if i < robot_distribution[0]:
                    robot_type = 0
                elif i < robot_distribution[0] + robot_distribution[1]:
                    robot_type = 1
                else:
                    robot_type = 2
                robot = Robot(position, i, robot_type=robot_type)
                robot._start_node = warehouse
                robots.append(robot)
                print("Robot {} of type {} with speed {} and capacity {} assigned to "
                      "warehouse".format(i, robot.type, robot.speed, robot.capacity, warehouse))

            print("\n\t Robots assigned.")
            bar.update(itr)
            itr += 1

            total_speed_capacity = 0
            for robot in robots:
                total_speed_capacity += robot.speed * robot.capacity

            print("Total capacity*speed:", total_speed_capacity)

            # Invoke the routing algorithm
            print("\n\t Routing robots...")

            timer_start = time.time()
            if routing_mode == "random_multiple":
                assignment_cost = route_multiple(world, robots, mode="random", number_of_runs=number_of_runs_for_random)
            else:
                assignment_cost = route(world, robots, mode=routing_mode)[1]
            timer_end = time.time()

            computation_time = timer_end - timer_start
            bar.update(itr)
            itr += 1

            filehandle.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\n' % (
                routing_mode, robot_distribution[0], robot_distribution[1],
                robot_distribution[2], assignment_cost, computation_time, total_speed_capacity))
