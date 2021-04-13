from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
import numpy as np
import matplotlib as mpl
import time

import progressbar

number_of_robots_for_varying_type = 10
robot_config_for_varying_number = np.array([1, 1, 0])
maximum_number_of_robots_for_varying_number = 30
number_of_runs_for_random_multiple = 20

results = {}

routing_modes = ["random",
                 "random_multiple",
                 "hungarian",
                 "linear_separate_tasks",
                 "linear_joined_tasks",
                 # "tsm",
                 # "home"
                 ]

timestr = time.strftime("%Y%m%d-%H%M%S")

if __name__ == "__main__":

    """
        Experiment with varying robot types.
    """
    '''
    robot_distributions = np.array([[number_of_robots_for_varying_type, 0, 0]])

    for i in range(number_of_robots_for_varying_type):
        robot_distributions = np.r_[robot_distributions, [[number_of_robots_for_varying_type - i - 1, i + 1, 0]]]

    print(robot_distributions)

    bar = progressbar.ProgressBar(max_value=len(routing_modes) * len(robot_distributions) * 3, redirect_stdout=True)
    itr = 1
    # bar = progressbar.

    # Open file
    filehandle = open('robot_type_results{}.txt'.format(timestr), 'w')
    filehandle.write('routing_mode\trobot_distribution\tassignment_cost\tcomputation_time\ttotal_speed_capacity\n')

    for routing_mode in routing_modes:
        for robot_distribution in robot_distributions:
            print("\n\t Running in", routing_mode, "routing mode with", number_of_robots_for_varying_type, "robots in",
                  robot_distribution, "configuration")

            print("\n\t Initialising world...")
            bar.update(itr)
            itr += 1
            world = World(number_of_hospitals=15)

            # Initialize the robots in the warehouse
            robots = []
            print("\n\t World created. Assigning robots to warehouses...\n")

            # Distribute robot types
            robot_distribution = np.round(number_of_robots_for_varying_type * robot_distribution / np.sum(robot_distribution))

            print("robot_distribution: ", robot_distribution)

            for i in range(number_of_robots_for_varying_type):
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
                assignment_cost = route_multiple(world, robots, mode="random", number_of_runs=number_of_runs_for_random_multiple)
            else:
                assignment_cost = route(world, robots, mode=routing_mode)[1]
            timer_end = time.time()

            computation_time = timer_end - timer_start
            bar.update(itr)
            itr += 1

            filehandle.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\n' % (
                routing_mode, robot_distribution[0], robot_distribution[1],
                robot_distribution[2], assignment_cost, computation_time, total_speed_capacity))

    filehandle.close()
    '''

    """
    Now experiment with varying robot number.
    """

    filehandle2 = open('robot_number_results{}.txt'.format(timestr), 'w')
    filehandle2.write('routing_mode\tnumber_of_robots\tassignment_cost\tcomputation_time\n')

    bar = progressbar.ProgressBar(max_value=maximum_number_of_robots_for_varying_number * len(routing_modes) * 3,
                              redirect_stdout=True)
    itr = 1

    for routing_mode in routing_modes:
        for n_robots in range(maximum_number_of_robots_for_varying_number):
            print("\n\t Running in", routing_mode, "routing mode with", n_robots + 1, "robots in",
                  robot_config_for_varying_number, "configuration")

            print("\n\t Initialising world...")
            bar.update(itr)
            itr += 1
            world = World(number_of_hospitals=15)

            # Initialize the robots in the warehouse
            robots = []
            print("\n\t World created. Assigning robots to warehouses...\n")

            # Distribute robot types
            robot_distribution = np.round(np.array([0.01, -0.01, -0.01]) + (n_robots + 1) *
                                          robot_config_for_varying_number / np.sum(robot_config_for_varying_number))

            print("robot_distribution: ", robot_distribution)

            for i in range(n_robots+1):
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
                assignment_cost = route_multiple(world, robots, mode="random", number_of_runs=number_of_runs_for_random_multiple)
            else:
                assignment_cost = route(world, robots, mode=routing_mode)[1]
            timer_end = time.time()

            computation_time = timer_end - timer_start
            bar.update(itr)
            itr += 1

            filehandle2.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
                routing_mode, robot_distribution[0], robot_distribution[1],
                robot_distribution[2], n_robots+1, assignment_cost, computation_time, total_speed_capacity))
