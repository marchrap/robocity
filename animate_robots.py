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

#fig = plt.gcf()
#ax = plt.gca()  # xlim=(-2, 2), ylim=(-2, 2))
#ax.set_aspect('equal')

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
        start_node = np.array(nodes[path_nodes[i]])
        end_node = np.array(nodes[path_nodes[i + 1]])

        difference_vector = end_node - start_node

        position = start_node
        position_list.append(position)

        t = 0
        while not np.allclose(position, end_node, atol=1e-02):  # and t < 100:
            # increment position in direction towards target
            position = position + speed * dt * difference_vector / np.linalg.norm(difference_vector)
            # print(position)
            t += dt
            position_list.append(position)
        # print(position)
        # print("t: ", t)

    return position_list

def animate_robots(world, robots, fig=plt.gcf(),ax=plt.gca()):
    """
    Parameters
    ----------
    world: World object.

    robots: list of Robot objects.

    fig: existing figure

    ax: existing axes
    """

    nodes = world.positions
    print(nodes)

    for robot in robots:
        path = create_path(robot, nodes)
        plot_paths.append(path)
    for robot in robots:
        robot_sprites.append(plt.Circle((0, 0), 0.025, color='firebrick'))
    for sprite in robot_sprites:
        ax.add_patch(sprite)

    ani = FuncAnimation(fig, update, frames=999, interval=20, blit=False)

    plt.show()