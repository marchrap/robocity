import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import networkx as nx
import cvxpy as cp
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import copy
"""
Takes the world and robots and creates routes for the robots, adding them to the path_of_node_integers list in each
robot object.
"""


def route(world, robots, mode="random"):
    """
    Routes the world demand and matches it with the robots.

    Parameters
    ----------
    world:          World object
        world object as defined in world.py
    robots:         list
        list of Robot objects that will be altered for the animation
    mode:           str
        a string that represents the mode we are going to use
    """
    # Obtain all the tasks
    tasks = {}
    for i, hospital in enumerate(world.hospitals):
        if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
            pointer = world.graph.nodes[hospital]
            tasks[hospital] = np.array([pointer['demand1'], pointer['demand2']], dtype=float)

    while True:
        # Obtain the assignments. Those should be in the form [[hospital_id, np.array([delivered1, delivered2])],...]
        assignments = routing_algorithm(world, robots, mode=mode)
        for i, robot_assignments in enumerate(assignments):
            for assignment in robot_assignments:
                # Unwrap the assignment
                hospital, delivered = assignment

                # Append the hospital to the given robot path
                robots[i]._node_path.append(hospital)

                # Update the tasks list and the world graph
                tasks[hospital] -= delivered
                world.graph.nodes[hospital]['demand1'] = max(0, tasks[hospital][0])
                world.graph.nodes[hospital]['demand2'] = max(0, tasks[hospital][1])
                if np.all(tasks[hospital] <= 0.):
                    del tasks[hospital]

            # Append the path to the origin
            robots[i]._node_path.append(robots[i]._start_node)

        if len(tasks.keys()) == 0:
            break

    # Conduct path routing
    flowtime = 0
    makespan = 0

    for i, robot in enumerate(robots):
        robot._current_node = robot.start_node
        total_path = []
        cost = 0
        for node in robot._node_path[:-1]:
            # Calculate the path and distance and update the current_node
            distance, path = nx.single_source_dijkstra(world.graph, robot._current_node, node, weight='length')
            total_path.extend(path)
            cost += distance / robot.speed
            robot._current_node = node

            # Update the flowtime and the makespan
            flowtime += cost
            if cost > makespan:
                makespan = cost

        # Update the robots path
        robot._node_path = total_path

    return flowtime, makespan


def routing_algorithm(world, robots, mode="random"):
    """
    Route the world using various algorithms.

    Parameters
    ----------
    world:          World object
        world object as defined in world.py
    robots:         list
        list of Robot objects that will be altered for the animation
    mode:           str
        a string that represents the mode we are going to use
    """
    assignments = [[] for _ in range(len(robots))]
    if mode == "random":
        """Assign each task to a random robot multiple times to find a distribution."""
        tasks = {}
        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
                pointer = world.graph.nodes[hospital]
                tasks[hospital] = np.array([pointer['demand1'], pointer['demand2']], dtype=float)

        # Assign robots to tasks until there are none left
        while len(tasks) > 0:
            print("Remaining tasks: ", tasks)
            for i, robot in enumerate(robots):
                if len(tasks) == 0:
                    break
                random_goal = random.choice(list(tasks.keys()))
                tasks[random_goal] -= np.array([robot.capacity, robot.capacity])
                assignments[i].append([random_goal, np.array([robot.capacity, robot.capacity])])
                if np.all(tasks[random_goal] <= 0.):
                    del tasks[random_goal]

    elif mode == "hungarian":
        """ We want a cost matrix of size number_of_robots x no_of_tasks"""
        number_of_robots = len(robots)
        tasks = []

        for hospital in world.hospitals:
            if world.graph.nodes[hospital]['demand1'] != 0:
                tasks.append((hospital, 0, world.graph.nodes[hospital]['demand1']))
            if world.graph.nodes[hospital]['demand2'] != 0:
                tasks.append((hospital, 1, world.graph.nodes[hospital]['demand2']))

        cost_matrix = np.zeros((number_of_robots, len(tasks)))

        # So now we have a list of tasks. Each task is a tuple: (hospital, demand type, demand)
        # We also have a cost matrix of the correct size, now we fill it in with the time cost
        for i, robot in enumerate(robots):
            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task[0], weight='length')

                # Calculate time taken to go to that hospital
                time_taken = path_length / robot.speed
                cost_matrix[i][j] = time_taken

        robot_ind, task_ind = linear_sum_assignment(cost_matrix)

        for i, index in enumerate(robot_ind):
            task = tasks[task_ind[i]]
            assignments[i].append([task[0], np.array([(1-task[1])*robots[index].capacity,
                                                      task[1]*robots[index].capacity])])

    elif mode == "linear_separate_tasks":
        # Takes all the tasks as separate tasks, i.e. does not join them together and the robot only delivers one type
        # of task.

        # Obtain all the demand and priority for goods 1 and 2
        demand = []
        tasks = []
        types = []
        priority = []
        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0:
                demand.append(world.graph.nodes[hospital]['demand1'])
                tasks.append(hospital)
                types.append(0)
                priority.append(world.graph.nodes[hospital]['priority'])
            if world.graph.nodes[hospital]['demand2'] != 0:
                demand.append(world.graph.nodes[hospital]['demand2'])
                tasks.append(hospital)
                types.append(1)
                priority.append(world.graph.nodes[hospital]['priority'])

        # Obtain the time cost matrix and the robots' capacity.
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
        nonzero = x.value.nonzero()
        for index in range(len(nonzero[0])):
            i = nonzero[1][index]
            j = nonzero[0][index]
            robot = robots[j]
            task = tasks[i]
            assignments[j].append([task, np.array([(1-types[i])*robot.capacity, types[i]*robot.capacity])])

    elif mode == "linear_joined_tasks":
        # As above but allows the robots to deliver two goods at the same time

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
        nonzero = x.value.nonzero()
        print(nonzero)
        for index in range(len(nonzero[0])):
            i = nonzero[1][index]
            j = nonzero[0][index]
            task = tasks[i]
            assignments[j].append([task, np.array([capacity[j][0], capacity[j][1]])])

    elif mode == "tsm":
        # Method based on the m-travelling salesmen problem

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

        costs = cp.max(cp.hstack(costs)) + cp.sum(cp.multiply(cp.pos(demand - sum(capacities)), priority))
        objective = cp.Minimize(costs)
        problem = cp.Problem(objective, constraints)
        problem.solve(verbose=True, solver=cp.CBC, numberThreads=8, maximumSeconds=60, allowablePercentageGap=10)

        # Assign the results to the robots and evaluate the costs
        for i, x_i in enumerate(x):
            print(f"variable {i + 1}: {x_i.value}")
            print(f"variable {i + 1}: {np.sum(x_i.value * distances[i])}")
            print(f"variable {i + 1}: {capacities[i].value}")

        for i, robot in enumerate(robots):
            start = np.argmax(x[i].value[0, :])
            node = np.argmax(x[i].value[start, :])
            while node != 0:
                if np.any(capacities[i].value[node-1] != 0):
                    task = tasks[node-1]
                    assignments[i].append([task, capacities[i].value[node-1]])
                node = np.argmax(x[i].value[node, :])

    elif mode == "home":
        # Home made method allowing to specify the depth of the solution to be considered N

        # Obtain all the demand and priority for goods 1 and 2
        demand = []
        tasks = []
        priority = []
        N = 2

        for i, hospital in enumerate(world.hospitals):
            if world.graph.nodes[hospital]['demand1'] != 0 or world.graph.nodes[hospital]['demand2'] != 0:
                pointer = world.graph.nodes[hospital]
                demand.append([pointer['demand1'], pointer['demand2']])
                tasks.append(hospital)
                priority.append([pointer['priority'], pointer['priority']])

        # Obtain the time cost matrix and the robots' capacity
        x = [[] for _ in range(len(robots))]
        capacities = []
        constraints = []
        costs = []

        for i, robot in enumerate(robots):
            # Obtain the time matrix for the robot
            time_matrix = np.zeros((len(demand), len(demand)))
            original = np.zeros(len(demand))
            for j, task in enumerate(tasks):
                path_length = nx.shortest_path_length(world.graph, robot.start_node, task, weight='length')
                original[j] = path_length / robot.speed

                for k, other_task in enumerate(tasks):
                    if other_task != task:
                        path_length = nx.shortest_path_length(world.graph, task, other_task, weight='length')
                        time_matrix[j][k] = path_length / robot.speed
                    else:
                        time_matrix[j][k] = 0

            # Add the initial state
            x[i].append(cp.Variable((len(demand), 1), boolean=True))
            constraints.append(cp.sum(x[i][0]) <= 1)
            costs.append(cp.sum(cp.multiply(cp.vec(x[i][0]), original)))
            capacities.append(cp.Variable((len(demand), 2), integer=True))

            # Loop over the other future states
            for n in range(1, N):
                x[i].append(cp.Variable((len(demand), 1), boolean=True))
                costs.append(cp.sum(cp.multiply(cp.pos(x[i][n - 1] + cp.transpose(x[i][n]) - 1), time_matrix)))
                constraints.append(cp.sum(x[i][n]) == cp.sum(x[i][0]))

            # Add the capacities constraints
            constraints.append(cp.sum(capacities[i], axis=0) <= robot.capacity)  # Make sure we are not over capacity
            constraints.append(cp.sum(capacities[i], axis=1) <= 1000*cp.vec(sum(x[i])))
            constraints.append(capacities[i] >= 0)

        demand = np.array(demand)
        priority = np.array(priority) * 10000

        costs = cp.max(cp.hstack(costs)) + cp.sum(cp.multiply(cp.pos(demand - sum(capacities)), priority))
        objective = cp.Minimize(costs)
        problem = cp.Problem(objective, constraints)
        problem.solve(verbose=True, solver=cp.CBC, numberThreads=8, maximumSeconds=60, allowablePercentageGap=5)

        # Assign the results to the robots and evaluate the costs
        for robot_i, robot in enumerate(x):
            print(f"ROBOT {robot_i}\n-------")
            print(f"delivered capacities: \n{capacities[robot_i].value}")
            print(f"step 0: {0}")
            for i, x_i in enumerate(robot):
                print(f"step {i + 1}: {x_i.value.T}")

        for i, robot in enumerate(robots):
            robot._current_node = robot.start_node
            for j, x_i in enumerate(x[i]):
                index = np.argmax(x_i.value)
                if np.any(capacities[i].value[index] != 0):
                    task = tasks[index]
                    assignments[i].append([task, capacities[i].value[index]])
                    robot._current_node = task

    else:
        raise NotImplementedError

    return assignments


def route_multiple(world, robots, mode="random", number_of_runs=1):
    """
    Routes the world demand and matches it with the robots like in the route method but multiple times to evaluate
    quantities such as mean, etc. Particularly useful for the random method.

    Parameters
    ----------
    world:          World object
        world object as defined in world.py
    robots:         list
        list of Robot objects that will be altered for the animation
    mode:           str
        a string that represents the mode we are going to use
    number_of_runs: int
        a number which dictates how many runs should be conducted on the given method
    """

    flowtimes = []
    makespans = []
    for i in range(number_of_runs):
        print(f"Run number {i + 1}")
        flowtime, makespan = route(copy.deepcopy(world), copy.deepcopy(robots), mode)
        flowtimes.append(flowtime)
        makespans.append(makespan)

    mean_assignment_cost = sum(makespans) / len(makespans)
    print("Average random maketime: ", round(mean_assignment_cost, 2))

    with open('random_assignment_costs.txt', 'w') as filehandle:
        for listitem in makespans:
            filehandle.write('%s\n' % listitem)

    axs = plt.gca()
    N, bins, patches = axs.hist(makespans, bins=40)
    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()
    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())
    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    # Now we format the y-axis to display percentage
    axs.yaxis.set_major_formatter(PercentFormatter(xmax=len(makespans)))
    axs.set_ylabel('Occurance')
    axs.set_xlabel('Maketime')
    plt.annotate("Mean assignment cost: %s" % mean_assignment_cost, xy=(0.05, 0.95), xycoords='axes fraction')

    return mean_assignment_cost