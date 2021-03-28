from numpy import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import networkx as nx
import osmnx as ox

"""
Takes the world and robots and creates routes for the robots, adding them to the path_of_node_integers list in each
robot object.
"""


def routing_algorithm(world, robots, mode="random"):
    """
    Parameters
    ----------
    world:  World object
        world object as defined in world.py
    robots: list
        list of Robot objects that will be altered for the animation
    mode:   str
        a string that represents the mode we are going to use
    """

    if mode == "random":
        """Assign each robot with a random goal."""
        print(world.hospitals)
        for robot in robots:
            random_goal = random.choice(world.hospitals)
            print(random_goal)
            #source = ox.get_nearest_node(world.graph, robot.position[::-1])
            source = robot.start_node
            print(source)
            #try:
            path = nx.astar_path(world.graph, source, random_goal, weight="travel_time")
            #path = ox.distance.shortest_path(world.graph, source, random_goal, weight='travel_time')
            #reverse_path = path.reverse()
            reverse_path = path
            reverse_path.reverse()
            path.extend(reverse_path)
            robot._node_path = path
            #except:
            #    print("Routing error.")
            #    continue

    elif mode == "hungarian":

        """ We want a cost matrix of size number_of_robots x no_of_tasks"""

        number_of_robots = len(robots)

        tasks = []

        print(world.hospitals)

        for hospital in world.hospitals:

            if world.graph.nodes[hospital]['demand1'] != 0:
                tasks.append((hospital, 'demand1', world.graph.nodes[hospital]['demand1']))

            if world.graph.nodes[hospital]['demand2'] != 0:
                tasks.append((hospital, 'demand2', world.graph.nodes[hospital]['demand2']))

        cost_matrix = np.zeros((number_of_robots, len(tasks)))

        print(tasks)

        # So now we have a list of tasks. Each task is a tuple: (hospital, demand type, demand)

        # We also have a cost matrix of the correct size, now we fill it in with the time cost

        for i, robot in enumerate(robots):

            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task[0], weight='length')

                # Calculate time taken to go to that hospital

                time_taken = path_length / robot.speed

                cost_matrix[i][j] = time_taken

        print(cost_matrix)

        # These may be the wrong way round?

        robot_ind, task_ind = linear_sum_assignment(cost_matrix)

        for i, index in enumerate(robot_ind):
            robots[index]._node_path = nx.shortest_path(world.graph, robots[index].start_node, tasks[i][0],
                                                        weight='length')

        assignment_cost = cost_matrix[robot_ind, task_ind].sum()

        print("Assignment cost: ", assignment_cost)

        # need to add second round / many more rounds of task allocation for remaining tasks

        # need to add better starting node allocation (currently defaults to 0)

    elif mode == "marcin's magic method":
        pass
