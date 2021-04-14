from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
from animate_robots import animate_robots, progress_bar, progress_bar2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import time

routing_modes = [#"random",
                 #"hungarian",
                 #"linear_separate_tasks",
                 #"linear_joined_tasks",
                 # "tsm",
                 # "home"
                 "imported"
                 ]

labels = ["Hungarian", "Binary", "mStep"]

robot_types = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
import_file = "robot_path20210414-233314.txt"

dt = 3

if __name__ == "__main__":

    number_of_graphs = len(routing_modes)

    fig, axs = plt.subplots(1, number_of_graphs, figsize=(number_of_graphs * 8, 8))

    # plt.ion()
    # plt.show()
    # plt.draw()
    # plt.pause(0.001)

    for index, routing_mode in enumerate(routing_modes):

        robots = []
        world = World()

        for i in range(10):
            robot = Robot(np.array([0, 0]), i, robot_type=robot_types[i])
            robot._start_node = np.random.choice(world.warehouses)
            robots.append(robot)

        print("\n\t Routing robots with {}...".format(routing_mode))
        if routing_mode == "imported":
            with open(import_file, 'r') as filehandle:
                for j, line in enumerate(filehandle):
                    line = line[:-1]
                    line_list = line.split('\t')
                    print(line_list)
                    if j == 0:
                        assignment_cost = float(line_list[3])
                        computation_time = float(line_list[5])
                    else:
                        robot = robots[j-1]
                        for string_element in line_list:
                            try:
                                element = float(string_element)
                                robot._node_path.append(element)
                            except ValueError:
                                element = string_element
        else:
            timer_start = time.time()
            assignment_cost = route(world, robots, mode=routing_mode)[1]
            timer_end = time.time()
            computation_time = timer_end - timer_start

        print(routing_mode, assignment_cost, computation_time)

        if type(axs) == np.ndarray:
            ax = axs[index]
        else:
            ax = axs

        ax.set_facecolor('black')
        world.plot(ax=ax, show=False)
        print("\n\t Calculating animation {}/{}...".format(index + 1, number_of_graphs))

        # plt.draw()
        # plt.pause(0.001)

        ani = animate_robots(world, robots, fig, ax, dt)
        ax.legend()

        ax.annotate("Routing method: %s" % routing_mode, xy=(0.05, 0.95), xycoords='axes fraction',
                    backgroundcolor='white')
        ax.annotate("Makespan: %.2f s" % assignment_cost, xy=(0.05, 0.90), xycoords='axes fraction',
                    backgroundcolor='white')
        ax.annotate("Computation time: %.2f ms" % (computation_time * 1000), xy=(0.05, 0.85), xycoords='axes fraction',
                    backgroundcolor='white')

        # fig.tight_layout()

        ax.annotate(labels[index], (0.5, -0.025), (0, 0), xycoords='axes fraction', textcoords='offset points',
                    va='top', ha='center', fontsize='x-large')

        # plt.draw()
        # plt.pause(0.001)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\maxw\\PycharmProjects\\4I15 MRS Robocity\\ffmpeg-4.4' \
                                            r'-full_build\\bin\\ffmpeg.exe '

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1)

    # print("Saving render...")
    # render = ani.save("animation%s.mp4" % timestr, fps=100, progress_callback=progress_bar)

    plt.show()
