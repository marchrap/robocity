from numpy import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import networkx as nx

"""
Takes the world and robots and creates routes for the robots, adding them to the path_of_node_integers list in each robot object

"""


def routing_algorithm(world, robots, mode="random"):
    """
    Parameters
    ----------
    world: World object.

    robots: list of Robot objects.
    """

    if mode == "random":
        for robot in robots:
            random_list = []
            # dummy paths for demonstration, this is just all nodes in a random order.
            for i in range(10):
                random_list.append(random.choice(list(world.positions.keys())))
            robot._node_path = random_list


    elif mode == "hungarian":
        """ We want a cost matrix of size number_of_robots x no_of_tasks"""

        number_of_robots = len(robots)

        no_of_tasks = 0
        tasks = []

        print(world.hospitals)

        for hospital in world.hospitals:
            '''if world.graph.nodes[hospital]['demand1'] == 1:
                tasks.append((hospital, 'demand1'))

            if world.graph.nodes[hospital]['demand2'] == 1:
                tasks.append((hospital, 'demand2'))'''

            tasks.append((hospital, 'demandX'))  # just to make it work

        cost_matrix = np.zeros((number_of_robots, len(tasks)))

        # So now we have a list of tasks. Each task is a tuple with the node and the type of demand
        # We also have a cost matrix of the correct size, now we fill it in with the time cost

        print(robots, tasks)

        for i, robot in enumerate(robots):
            for j, task in enumerate(tasks):
                # Calculate time taken to go to that hospital
                time_taken = robot.speed * nx.astar_path_length(world.graph, robot.start_node, task[0])
                cost_matrix[i][j] = time_taken

        print(cost_matrix)

        # These may be the wrong way round?
        robot_ind, task_ind = linear_sum_assignment(cost_matrix)
        print(robot_ind, task_ind)

        for i in robot_ind:
            for j in task_ind:
                robots[i]._node_path = nx.astar_path(world.graph, robot.start_node, tasks[j][0])

        # need to add second round / many more rounds of task allocation for remaining tasks
        # need to add better starting node allocation (currently defaults to 0)

    elif mode == "marcin's magic method":
        pass
