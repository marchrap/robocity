from numpy import random

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
        pass

    elif mode == "marcin's magic method":
        pass
