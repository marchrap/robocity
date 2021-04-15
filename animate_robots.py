import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_config import Robot
from progressbar import ProgressBar

"""
Takes world and robots, plots the world, then plots animations of robots path_of_node_integers on top.
"""

robot_sprites = []
line_sprites = []
plot_paths = []


def update(i, fig):
    try:
        for j in range(len(robot_sprites)):
            try:
                robot_sprites[j].center = plot_paths[j][i]
            except:
                continue
        for j in range(len(line_sprites)):
            try:
                if plot_paths[j][:i]:
                    line_sprites[j][0].set_data(*zip(*plot_paths[j][:i]))
            except:
                continue
    except:
        pass


def create_path(robot, world, dt):
    position_list = []
    path_nodes = robot.node_path
    speed = robot.speed

    print("Calculating path for robot: ", robot.ID)

    for i in range(len(path_nodes) - 1):
        # print("Calculating path: ", i)
        start_pointer = world.graph.nodes[path_nodes[i]]
        end_pointer = world.graph.nodes[path_nodes[i + 1]]

        start_node = np.array([start_pointer['x'], start_pointer['y']])
        end_node = np.array([end_pointer['x'], end_pointer['y']])

        difference_vector = end_node - start_node

        position = start_node
        position_list.append(position)

        # print(position, end_node)

        t = 0
        while not np.allclose(position, end_node, atol=dt * speed):  # and t < 100:
            # increment position in direction towards target
            position = position + speed * dt * difference_vector / np.linalg.norm(difference_vector)
            # print(position)
            # print("t: ", t)
            t += dt
            position_list.append(position)
        # print(position)
        # print("t: ", t)
    # print(position_list)
    return position_list


def animate_robots(world, robots, fig=plt.gcf(), ax=plt.gca(), dt=1):
    """
    Parameters
    ----------
    world: World object.

    robots: list of Robot objects.

    fig: existing figure

    ax: existing axes
    """

    # new_robot_sprites = []
    # line_sprites = []
    # plot_paths = []

    for robot in robots:
        path = create_path(robot, world, dt)
        plot_paths.append(path)
        start_pointer = world.graph.nodes[robot.start_node]
        origin = np.array([start_pointer['x'], start_pointer['y']])
        r = np.random.random()
        b = np.random.random()
        g = np.random.random()
        colour = (r, g, b)
        sprite = plt.Circle(origin, 40, color=colour, zorder=3, label=f'robot {robot.ID}, type: {robot.type}',
                            alpha=.9)
        line_sprites.append(ax.plot([], [], color=colour, alpha=.75, linewidth=2))
        # plt.plot(*zip(*path), color=colour, alpha=.5)
        print("path: ", robot._node_path)
        ax.add_patch(sprite)
        robot_sprites.append(sprite)
        # new_robot_sprites.append(sprite)

    # for sprite in robot_sprites:
    #    ax.add_patch(sprite)

    # print(robot_sprites)
    # print(plot_paths)
    # print(line_sprites)

    max_route_len = max([len(x) for x in plot_paths])
    print(f'Max number of points in a route : {max_route_len}')

    ani = FuncAnimation(fig, update, frames=max_route_len, fargs=[fig], interval=20, blit=False)

    return ani
    # plt.show()


# def progress_callback(current_frame, total_frames):
#    with ShadyBar('Processing', max=total_frames) as bar:
#        for current_frame in range(total_frames):
#            # Do some work
#            bar.next()


# bar = IncrementalBar('Processing', max=max([len(x) for x in plot_paths]))


def progress_bar(current_frame, total_frames):
    print("Frame {}/{}".format(current_frame + 1, total_frames))


def progress_bar2(current_frame, total_frames):
    bar = ProgressBar()
    if current_frame == 0:
        bar = ProgressBar(max_value=total_frames, redirect_stdout=True)
    bar.update(current_frame)
