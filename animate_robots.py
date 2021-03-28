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
    try:
        for j in range(len(robot_sprites)):
            try:
                robot_sprites[j].center = plot_paths[j][i]
                print("i: %d, j: %d" % (i, j))
            except:
                continue
    except:
        pass


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
        while not np.allclose(position, end_node, atol=1e-03):  # and t < 100:
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
        start_pointer = world.graph.nodes[robot.start_node]
        origin = np.array([start_pointer['x'], start_pointer['y']])
        #if robot._type == 0:
        #    robot_sprites.append(plt.Circle(origin, 15, color='darkcyan', zorder=3, label=f'robot {robot.ID}, type: {robot.type}', alpha=.75))
        #if robot._type == 1:
        r = np.random.random()
        b = np.random.random()
        g = np.random.random()
        colour = (r, g, b)
        robot_sprites.append(plt.Circle(origin, 0.0001, color=colour, zorder=3, label=f'robot {robot.ID}, type: {robot.type}', alpha=.75))
    for sprite in robot_sprites:
        ax.add_patch(sprite)

    print(robot_sprites)
    print(plot_paths)

    max_route_len = max([len(x) for x in plot_paths])
    print(f'Max number of nodes in a route : {max_route_len}')

    ani = FuncAnimation(fig, update, frames=max_route_len, interval=20, blit=False)

    return ani
    #plt.show()