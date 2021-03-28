import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_config import Robot

"""
Takes world and robots, plots the world, then plots animations of robots path_of_node_integers on top.
"""

robot_sprites = []
plot_paths = []

dt = 0.001

def update(i):
    for j in range(len(robot_sprites)):
        robot_sprites[j].center = plot_paths[j][i]
        print("i: %d, j: %d" % (i, j))
        #print("point: ", plot_paths[j][i])

def create_path(robot, world):
    position_list = []
    path_nodes = robot.node_path
    speed = robot.speed

    for i in range(len(path_nodes) - 1):
        # print("i: ", i)
        start_pointer = world.graph.nodes[path_nodes[i]]
        end_pointer = world.graph.nodes[path_nodes[i + 1]]

        start_node = np.array([start_pointer['x'], start_pointer['y']])
        end_node = np.array([end_pointer['x'], end_pointer['y']])

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
    print(position_list)
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

    for robot in robots:
        path = create_path(robot, world)
        plot_paths.append(path)
        if robot._type == 0:
            robot_sprites.append(plt.Circle((0, 0), 0.0001, color='darkcyan', zorder=3))
        if robot._type == 1:
            robot_sprites.append(plt.Circle((0, 0), 0.0001, color='cyan', zorder=3))
    for sprite in robot_sprites:
        ax.add_patch(sprite)

    print(robot_sprites)
    print(plot_paths)

    ani = FuncAnimation(fig, update, frames=240, interval=20, blit=False)

    return ani
    #plt.show()