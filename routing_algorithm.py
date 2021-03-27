import random

"""
Takes the world and robots and creates routes for the robots, adding them to the path_of_node_integers list in each robot object

"""


def routing_alorithm(world, robots):
    """
    Parameters
    ----------
    world: World object.

    robots: list of Robot objects.
    """

    for robot in robots:
        # dummy paths for demonstration, this is just all nodes in order.
        robot._node_path = list(world.positions.keys())
