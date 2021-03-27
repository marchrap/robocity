import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_config import Robot

"""
Takes world and robots, plots the world, then plots animations of robots path_of_node_integers on top.
"""

robot_sprites = []
plot_paths = []

dt = 0.01

fig = plt.figure()
ax = plt.axes()  # xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal')

def update(i):
    for j in range(len(robot_sprites)):
        robot_sprites[j].center = plot_paths[j][i]
        print("i: %d, j: %d" % (i, j))
        print("point: ", plot_paths[j][i])

def create_path(robot, nodes):
    position_list = []
    path_nodes = robot.node_path
    speed = robot.speed

    for i in range(len(path_nodes) - 1):
        # print("i: ", i)
        start_node = nodes[path_nodes[i]]
        end_node = nodes[path_nodes[i + 1]]
        # print("start_node: ", path_nodes[i], start_node.position)
        # print("end_node: ", path_nodes[i+1], end_node.position)

        difference_vector = end_node.position - start_node.position
        # print(difference_vector, np.linalg.norm(difference_vector), difference_vector / np.linalg.norm(difference_vector))

        position = start_node.position
        position_list.append(position)

        t = 0
        while not np.allclose(position, end_node.position, atol=1e-02):  # and t < 100:
            # increment position in direction towards target
            position = position + speed * dt * difference_vector / np.linalg.norm(difference_vector)
            # print(position)
            t += dt
            position_list.append(position)
        # print(position)
        # print("t: ", t)

    return position_list

def animate_robots(world, robots):
    """
    Parameters
    ----------
    world: World object.

    robots: list of Robot objects.
    """

    nodes = world.positions

    for robot in robots:
        path = create_path(robot)
        plot_paths.append(path)
    for robot in robots:
        robot_sprites.append(plt.Circle((0, 0), 0.1, color='lightblue'))
    for sprite in robot_sprites:
        ax.add_patch(sprite)

    ani = FuncAnimation(fig, update, frames=999, interval=20, blit=False)

    plt.show()