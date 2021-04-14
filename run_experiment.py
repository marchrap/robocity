from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
import numpy as np
import matplotlib as mpl
import time
import progressbar
from math import ceil

""" Select experiments """

test_methods = 1
test_varying_robot_types = 0
test_varying_robot_numbers = 0
test_demand_changes = 0

"""
test_methods:
This will run just a 15 hospital world with 10 robots.
"""

"""
test_varying_robot_types:
This will run a 15 hospital world with 10 robots of a combination of type 0 and 1
"""

number_of_robots_for_varying_type = 10

"""
test_varying_robot_numbers:
This will run a 15 hospital world with an increasing number of robots. 
"""

robot_config_for_varying_number = np.array([1, 1, 0])
maximum_number_of_robots_for_varying_number = 30

"""
test_demand_changes:
This will run a 15 hospital world with increasing demands.
"""

number_of_robots_for_varying_demand = 10
robot_config_for_varying_demand = np.array([1, 1, 0])
maximum_maximum_hospital_demand = 30
maximum_hospital_demand_step = 1

""" Used in all tests """
number_of_runs_for_random_multiple = 25

""" Routing modes to analyse, comment as appropriate """

routing_modes = ["random",
                 "random_multiple",
                 "hungarian",
                 "linear_separate_tasks",
                 "linear_joined_tasks",
                 "tsm_short"
                 "tsm",
                 "home"
                 ]

timestr = time.strftime("%Y%m%d-%H%M%S")
titlestr = "routing_mode\trobot_distribution\tnumber_of_robots\tmax_demand\ttotal_speed_capacity\tflowtime\tmakespan" \
           "\tscore\tcomputation_time\n "

if __name__ == "__main__":

    if test_methods:

        print("\n\tTesting methods only.")

        robot_distribution = np.array([1, 1, 0])
        bar = progressbar.ProgressBar(max_value=len(routing_modes) * 3, redirect_stdout=True)
        itr = 1
        # Open file
        filehandle0 = open('method_comparison_results{}.txt'.format(timestr), 'w')
        filehandle0.write(titlestr)

        for routing_mode in routing_modes:
            print("\n\t Running in", routing_mode, "routing mode with", number_of_robots_for_varying_type, "robots in",
                  robot_distribution, "configuration")
            maximum_maximum_hospital_demand + 1
            print("\n\t Initialising world...")
            bar.update(itr)
            itr += 1
            world = World(number_of_hospitals=15)

            # Initialize the robots in the warehouse
            robots = []
            print("\n\t World created. Assigning robots to warehouses...\n")

            # Distribute robot types
            robot_distribution = np.round(
                number_of_robots_for_varying_type * robot_distribution / np.sum(robot_distribution))

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
                makespan, flowtime, score = route_multiple(world, robots, mode="random",
                                                           number_of_runs=number_of_runs_for_random_multiple)
            elif routing_mode == "tsm_short":
                flowtime, makespan, score = route(world, robots, mode="tsm", maximumSeconds=60)
            else:
                flowtime, makespan, score = route(world, robots, mode=routing_mode)
            timer_end = time.time()

            computation_time = timer_end - timer_start
            bar.update(itr)
            itr += 1

            filehandle0.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
                routing_mode, robot_distribution[0], robot_distribution[1],
                robot_distribution[2], number_of_robots_for_varying_type, 3, total_speed_capacity,
                makespan, flowtime, score, computation_time))

        filehandle0.close()
        bar.finish()

    """
        Experiment with varying robot types.
    """

    if test_varying_robot_types:

        print("\n\tTesting varying_robot_types.")

        robot_distributions = np.array([[number_of_robots_for_varying_type, 0, 0]])

        for i in range(number_of_robots_for_varying_type):
            robot_distributions = np.r_[robot_distributions, [[number_of_robots_for_varying_type - i - 1, i + 1, 0]]]

        print(robot_distributions)

        bar = progressbar.ProgressBar(max_value=len(routing_modes) * len(robot_distributions) * 3, redirect_stdout=True)
        itr = 1
        # bar = progressbar.

        # Open file
        filehandle1 = open('robot_type_results{}.txt'.format(timestr), 'w')
        filehandle1.write(titlestr)

        for routing_mode in routing_modes:
            for robot_distribution in robot_distributions:
                print("\n\t Running in", routing_mode, "routing mode with", number_of_robots_for_varying_type,
                      "robots in",
                      robot_distribution, "configuration")

                print("\n\t Initialising world...")
                bar.update(itr)
                itr += 1
                world = World(number_of_hospitals=15)

                # Initialize the robots in the warehouse
                robots = []
                print("\n\t World created. Assigning robots to warehouses...\n")

                # Distribute robot types
                robot_distribution = np.round(
                    number_of_robots_for_varying_type * robot_distribution / np.sum(robot_distribution))

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
                    makespan, flowtime, score = route_multiple(world, robots, mode="random",
                                                               number_of_runs=number_of_runs_for_random_multiple)
                else:
                    flowtime, makespan, score = route(world, robots, mode=routing_mode)
                timer_end = time.time()

                computation_time = timer_end - timer_start
                bar.update(itr)
                itr += 1

                filehandle1.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
                    routing_mode, robot_distribution[0], robot_distribution[1],
                    robot_distribution[2], number_of_robots_for_varying_type, 3, total_speed_capacity,
                    makespan, flowtime, score, computation_time))

        filehandle1.close()
        bar.finish()

    """
    Now experiment with varying robot number.
    """

    if test_varying_robot_numbers:

        print("\n\tTesting robot number.")

        filehandle2 = open('robot_number_results{}.txt'.format(timestr), 'w')
        filehandle2.write(titlestr)

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

                for i in range(n_robots + 1):
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
                    makespan, flowtime, score, = route_multiple(world, robots, mode="random",
                                                                number_of_runs=number_of_runs_for_random_multiple)
                else:
                    flowtime, makespan, score, = route(world, robots, mode=routing_mode)
                timer_end = time.time()

                computation_time = timer_end - timer_start
                bar.update(itr)
                itr += 1

                filehandle2.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
                    routing_mode, robot_distribution[0], robot_distribution[1],
                    robot_distribution[2], n_robots + 1, 3, total_speed_capacity,
                    makespan, flowtime, score, computation_time))

        filehandle2.close()
        bar.finish()

    """
    Now increase demand.
    """

    if test_demand_changes:

        print("\n\tTesting demand changes.")

        filehandle3 = open('increased_demand_results{}.txt'.format(timestr), 'w')
        filehandle3.write(titlestr)

        bar = progressbar.ProgressBar(
            max_value=ceil((maximum_maximum_hospital_demand + 1) * len(routing_modes) * 3 / maximum_hospital_demand_step),
            redirect_stdout=True)
        itr = 1

        for routing_mode in routing_modes:
            for max_demand in range(3, maximum_maximum_hospital_demand + 1, maximum_hospital_demand_step):
                print("\n\t Running in", routing_mode, "routing mode with", number_of_robots_for_varying_demand,
                      "robots in",
                      robot_config_for_varying_demand, "configuration. Maximum demand is", max_demand)

                print("\n\t Initialising world...")
                bar.update(itr)
                itr += 1
                world = World(number_of_hospitals=15, max_demand=max_demand)

                # Initialize the robots in the warehouse
                robots = []
                print("\n\t World created. Assigning robots to warehouses...\n")

                # Distribute robot types
                robot_distribution = np.round(np.array([0.01, -0.01, -0.01]) + number_of_robots_for_varying_demand *
                                              robot_config_for_varying_demand / np.sum(robot_config_for_varying_demand))

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
                    makespan, flowtime, score = route_multiple(world, robots, mode="random",
                                                               number_of_runs=number_of_runs_for_random_multiple)
                else:
                    flowtime, makespan, score = route(world, robots, mode=routing_mode)
                timer_end = time.time()

                computation_time = timer_end - timer_start
                bar.update(itr)
                itr += 1

                filehandle3.write('%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (
                    routing_mode, robot_distribution[0], robot_distribution[1],
                    robot_distribution[2], number_of_robots_for_varying_type, max_demand, total_speed_capacity,
                    makespan, flowtime, score, computation_time))

        filehandle3.close()
        bar.finish()

    print("\n\tExperiment complete.")
