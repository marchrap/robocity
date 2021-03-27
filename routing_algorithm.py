from numpy import random
import numpy as np
from scipy.optimize import linear_sum_assignment

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

        for hospital in world.hospitals:

            #no_of_tasks += self.graph.nodes[hospital]['demand1'] + self.graph.nodes[hospital]['demand2']

            if self.graph.nodes[hospital]['demand1'] == 1:

                tasks.append((hospital, 'demand1'))

            if self.graph.nodes[hospital]['demand2'] == 1:

                tasks.append((hospital, 'demand2'))

        cost_matrix = np.zeros((number_of_robots, len(tasks)))

        # So now we have a list of tasks. Each task is a tuple with the node and the type of demand
        # We also have a cost matrix of the correct size, now we fill it in with the time cost

        for i, robot in enumerate(robots):
            for j in range(len(tasks)):

                # Calculate time taken to go to that hospital
                time_taken = robot.speed """ HOW DO I GET THE DISTANCE BETWEEN TWO NODES HERE"""
                cost_matrix[i][j] = time_taken

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

    elif mode == "marcin's magic method":
        pass
