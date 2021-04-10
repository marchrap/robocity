from numpy import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import networkx as nx
import osmnx as ox
import time
import cvxpy as cp

"""
Takes the world and robots and creates routes for the robots, adding them to the path_of_node_integers list in each
robot object.
"""

# TODO change the timing so that traffic and speed limits are taken into account
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

        assignment_cost = 0.0

        # print(world.hospitals)
        for robot in robots:
            random_goal = random.choice(world.hospitals)
            # print(random_goal)
            # source = ox.get_nearest_node(world.graph, robot.position[::-1])
            source = robot.start_node
            # print(source)
            try:
                path = nx.astar_path(world.graph, source, random_goal, weight='length')
                # path = ox.distance.shortest_path(world.graph, source, random_goal, weight='travel_time')
                end_path = []
                for i in path:
                    end_path.append(i)
                path.reverse()
                for i in path:
                    end_path.append(i)
                robot._node_path = end_path

                path_length = nx.astar_path_length(world.graph, source, random_goal, weight='length')

                assignment_cost += path_length / robot.speed

            except:
                print("Routing error.")
                continue

        print("Total flowtime: ", assignment_cost)

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

        print(robot_ind)
        print(task_ind)

        for i, index in enumerate(robot_ind):
            path = nx.shortest_path(world.graph, robots[index].start_node, tasks[i][0],
                                    weight='length')
            end_path = []
            for j in path:
                end_path.append(j)
            path.reverse()
            for j in path:
                end_path.append(j)
            robots[index]._node_path = end_path

        assignment_cost = cost_matrix[robot_ind, task_ind].sum()

        print("Total flowtime: ", assignment_cost)

        # need to add second round / many more rounds of task allocation for remaining tasks

        # need to add better starting node allocation (currently defaults to 0)

    elif mode == "magic1":
        # Obtain all the demand and priority for goods 1 and 2
        demand = []
        tasks = []
        priority = []
        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0:
                demand.append(world.graph.nodes[hospital]['demand1'])
                tasks.append(hospital)
                priority.append(world.graph.nodes[hospital]['priority'])
            if world.graph.nodes[hospital]['demand2'] != 0:
                demand.append(world.graph.nodes[hospital]['demand2'])
                tasks.append(hospital)
                priority.append(world.graph.nodes[hospital]['priority'])

        # Obtain the time cost matrix and the robots' capacity
        # TODO change the robots to allow them maybe move from one hospital to the next without rebasing and to hold
        #   different supplies.
        T = np.zeros((len(robots), len(demand)))
        capacity = np.zeros(len(robots))
        for i, robot in enumerate(robots):
            capacity[i] = robot.capacity
            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task, weight='length')
                time_taken = path_length / robot.speed
                T[i][j] = time_taken

        # Change the demand and priority arrays to numpy ones
        demand = np.array(demand)
        priority = np.array(priority)*10000

        # Define the optimization problem
        x = cp.Variable((len(robots), len(demand)), boolean=True)
        cost = cp.sum(cp.multiply(T, x)) + cp.sum(cp.neg(cp.multiply(cp.matmul(capacity, x) - demand, priority)))
        objective = cp.Minimize(cost)
        inequality = [cp.sum(x, axis=1) <= 1]
        problem = cp.Problem(objective, inequality)
        problem.solve()

        # Assign the results to the robots and evaluate the costs
        # print(x.value)
        nonzero = x.value.nonzero()
        assignment_cost = 0
        for index in range(len(nonzero[0])):
            robot = robots[nonzero[0][index]]
            task = tasks[nonzero[1][index]]
            robot._node_path = nx.shortest_path(world.graph, robot.start_node, task, weight='length')
            assignment_cost += T[nonzero[0][index]][nonzero[1][index]]

    elif mode == "magic2":
        # Obtain all the demand and priority for goods 1 and 2
        demand = []
        tasks = []
        priority = []

        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
                pointer = world.graph.nodes[hospital]
                demand.append([pointer['demand1'], pointer['demand2']])
                tasks.append(hospital)
                priority.append([pointer['priority'], pointer['priority']])

        # Obtain the time cost matrix and the robots' capacity
        # TODO change the robots to allow them maybe move from one hospital to the next without rebasing and to hold
        #   different supplies.
        T = np.zeros((len(robots), len(demand)))
        capacity = np.zeros((len(robots), 2))

        for i, robot in enumerate(robots):
            capacity[i, 0] = robot.capacity
            capacity[i, 1] = robot.capacity
            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task, weight='length')
                time_taken = path_length / robot.speed
                T[i][j] = time_taken

        # Change the demand and priority arrays to numpy ones
        demand = np.array(demand)
        priority = np.array(priority) * 10000

        # Define the optimization problem
        x = cp.Variable((len(robots), len(demand)), boolean=True)
        cost = cp.sum(cp.multiply(T, x)) + cp.sum(cp.neg(cp.multiply(cp.matmul(cp.transpose(x), capacity) - demand, priority)))
        objective = cp.Minimize(cost)
        inequality = [cp.sum(x, axis=1) <= 1]
        problem = cp.Problem(objective, inequality)
        problem.solve()

        # Assign the results to the robots and evaluate the costs
        # print(x.value)
        nonzero = x.value.nonzero()
        assignment_cost = 0

        for index in range(len(nonzero[0])):
            robot = robots[nonzero[0][index]]
            task = tasks[nonzero[1][index]]
            robot._node_path.extend(nx.shortest_path(world.graph, robot.start_node, task, weight='length'))
            assignment_cost += T[nonzero[0][index]][nonzero[1][index]]

    elif mode == "magic3":
        # Obtain all the demand and priority for goods 1 and 2
        robots = robots[:1]
        demand = []
        tasks = []
        priority = []

        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
                pointer = world.graph.nodes[hospital]
                demand.append([pointer['demand1'], pointer['demand2']])
                tasks.append(hospital)
                priority.append([pointer['priority'], pointer['priority']])

        # Obtain the time cost matrix and the robots' capacity
        # TODO change the robots to allow them maybe move from one hospital to the next without rebasing and to hold
        #   different supplies.
        T = np.zeros((len(robots), len(demand)))
        capacity = np.zeros((len(robots), 2))
        G = np.zeros((len(demand), len(demand)))
        for i, robot in enumerate(robots):
            capacity[i, 0] = robot.capacity
            capacity[i, 1] = robot.capacity
            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task, weight='length')
                time_taken = path_length / robot.speed
                T[i][j] = time_taken
                for k, other_task in enumerate(tasks):
                    if other_task != task:
                        path_length = nx.shortest_path_length(world.graph, task, other_task, weight='length')
                        time_taken = path_length / robot.speed
                        G[j][k] = time_taken / 2
                    else:
                        G[j][k] = 100000
        print(G.shape)


        # Change the demand and priority arrays to numpy ones
        demand = np.array(demand)
        priority = np.array(priority) * 10000
        print(T)
        # Define the optimization problem
        x = cp.Variable((len(robots), len(demand)), boolean=True)
        y = cp.Variable((len(robots), len(demand)), boolean=True)
        w = cp.Variable(len(demand), pos=True)
        zeros = np.eye(len(demand))/10000
        total = np.array(np.concatenate((np.concatenate((zeros, G), axis=1), np.concatenate((G, zeros), axis=1))))
        print(total)
        c = cp.Variable((len(demand), 2), integer=True)
        # print(.shape)
        cost_next = cp.quad_form(cp.transpose(cp.hstack([x[0, :], y[0, :]])), total)
        cost = cp.sum(cp.multiply(T, x)) + cost_next + cp.sum(cp.norm1(cp.multiply(c - demand, priority)))
        objective = cp.Minimize(cost)
        print(capacity)
        inequality = [cp.sum(x, axis=1) <= 1, cp.sum(c, axis=2) <= capacity, cp.sum(c, axis=1) <= 1000*cp.vec(x), c >= 0]
        problem = cp.Problem(objective, inequality)
        problem.solve()

        # Assign the results to the robots and evaluate the costs
        print(x.value)
        print(c.value)
        nonzero = x.value.nonzero()
        assignment_cost = 0

        for index in range(len(nonzero[0])):
            robot = robots[nonzero[0][index]]
            task = tasks[nonzero[1][index]]
            robot._node_path = nx.shortest_path(world.graph, robot.start_node, task, weight='length')
            assignment_cost += T[nonzero[0][index]][nonzero[1][index]]

    elif mode == "magic4":
        # Obtain all the demand and priority for goods 1 and 2
        demand = []
        tasks = []
        priority = []

        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
                pointer = world.graph.nodes[hospital]
                demand.append([pointer['demand1'], pointer['demand2']])
                tasks.append(hospital)
                priority.append([pointer['priority'], pointer['priority']])

        # Obtain the time cost matrix and the robots' capacity
        # TODO change the robots to allow them maybe move from one hospital to the next without rebasing and to hold
        #   different supplies.
        x = []
        v = []
        z = []
        capacities = []
        distances = []
        constraints = []
        costs = []
        for i, robot in enumerate(robots):
            # Create necessary variables
            x.append(cp.Variable((len(demand) + 1, len(demand) + 1), boolean=True))
            v.append(cp.Variable(len(demand) + 1, boolean=True))
            z.append(cp.Variable((len(demand), 1)))
            capacities.append(cp.Variable((len(demand), 2)))

            # Add constraints
            constraints.append(cp.sum(x[i], axis=1) == v[i])  # Note if city is moved from
            constraints.append(cp.sum(x[i], axis=0) == cp.sum(x[i], axis=1))  # Note if city is visited
            constraints.append(z[i] - cp.transpose(z[i]) + len(demand) * x[i][1:, 1:] <= len(demand) - 1)
            constraints.append(cp.sum(x[i], axis=1) <= cp.sum(x[i][0, :]))  # We start from 0th node
            constraints.append(cp.sum(capacities[i], axis=0) <= robot.capacity)  # Make sure we are not over capacity
            constraints.append(cp.sum(capacities[i], axis=1) <= 1000*v[i][1:])  # Check how many units are delivered
            constraints.append(capacities[i] >= 0)

            # Fill in the distance matrix
            distances.append(np.zeros((len(demand) + 1, len(demand) + 1)))
            for j, task in enumerate([robot.start_node] + tasks):
                for k, other_task in enumerate([robot.start_node] + tasks):
                    if other_task != task:
                        path_length = nx.shortest_path_length(world.graph, task, other_task, weight='length')
                        distances[i][j][k] = path_length / robot.speed
                    else:
                        distances[i][j][k] = 100000

            costs.append(cp.sum(cp.multiply(x[i], distances[i])))

        demand = np.array(demand)
        priority = np.array(priority) * 10000

        costs = cp.sum(cp.hstack(costs)) + cp.sum(cp.multiply(cp.norm1(demand - sum(capacities)), priority))
        objective = cp.Minimize(costs)
        problem = cp.Problem(objective, constraints)
        problem.solve(verbose=True)

        # Assign the results to the robots and evaluate the costs
        for i, x_i in enumerate(x):
            print(f"variable {i + 1}: {x_i.value}")
            print(f"variable {i + 1}: {np.sum(x_i.value * distances[i])}")
            print(f"variable {i + 1}: {capacities[i].value}")
        assignment_cost = 0

        # for i in range(len(robots)):
        #     if x[i][1, :]:
        #
        #     for row in x[i]:
        #
        #     robot = robots[[0][index]]
        #     task = tasks[nonzero[1][index]]
        #     robot._node_path = nx.shortest_path(world.graph, robot.start_node, task, weight='length')
        #     cost += T[nonzero[0][index]][nonzero[1][index]]
        #     if cost > assignment_cost:
        #         assignment_cost = cost

    return assignment_cost


def maxs_attempt_at_robot_return(world, robots, mode="random"):

    visited_hospitals = []

    # first round of assignment
    assignment_cost = routing_algorithm(world, robots, mode=mode)


    for robot in robots:
        visited_hospitals.append(robot.node_path[-1])
        return_path = nx.astar_path(world.graph, robot.node_path[-1], robot.start_node, weight = 'length')
        robot._node_path.extend(return_path)

    #print(visited_hospitals)
    #print(world.hospitals)

    # remove completed tasks
    for hospital in world.hospitals:
        if hospital in visited_hospitals:
            pointer = world.graph.nodes[hospital]
            print("Node {} visited, clearing demands.".format(hospital))
            pointer['demand1'] = 0
            pointer['demand2'] = 0

    # reassign robots to incomplete tasks
    assignment_cost += routing_algorithm(world, robots, mode=mode)

    for robot in robots:
        return_path = nx.astar_path(world.graph, robot.node_path[-1], robot.start_node, weight='length')
        robot._node_path.extend(return_path)

    return assignment_cost