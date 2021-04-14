from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
from animate_robots import animate_robots
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import time

routing_modes = ["random",
                 "hungarian",
                 "linear_separate_tasks",
                 # "linear_joined_tasks",
                 # "tsm",
                 # "home"
                 ]

robot_types = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

dt = 50

if __name__ == "__main__":

    number_of_graphs = len(routing_modes)

    fig, axs = plt.subplots(1, number_of_graphs, figsize=(number_of_graphs * 8, 8))

    #plt.ion()
    #plt.show()
    #plt.draw()
    #plt.pause(0.001)

    for index, routing_mode in enumerate(routing_modes):

        robots = []
        world = World()

        for i in range(10):
            robot = Robot(np.array([0, 0]), i, robot_type=robot_types[i])
            robot._start_node = np.random.choice(world.warehouses)
            robots.append(robot)

        print("\n\t Routing robots with {}...".format(routing_mode))
        timer_start = time.time()
        assignment_cost = route(world, robots, mode=routing_mode)[1]
        timer_end = time.time()
        computation_time = timer_end - timer_start

        print("Hey 1")

        if type(axs) == np.ndarray:
            ax = axs[index]
        else:
            ax = axs

        print("Hey 2")
        ax.set_facecolor('black')
        print("Hey 3")
        world.plot(ax=ax, show=False)
        print("\n\t Calculating animation {}/{}...".format(index + 1, number_of_graphs))

        plt.draw()
        plt.pause(0.001)

        ani = animate_robots(world, robots, fig2, ax, dt)
        ax.legend()

        ax.annotate("Routing method: %s" % routing_mode, xy=(0.05, 0.95), xycoords='axes fraction',
                    backgroundcolor='white')
        ax.annotate("Makespan: %.2f s" % assignment_cost, xy=(0.05, 0.90), xycoords='axes fraction',
                    backgroundcolor='white')
        ax.annotate("Computation time: %.2f ms" % (computation_time * 1000), xy=(0.05, 0.85), xycoords='axes fraction',
                    backgroundcolor='white')

        plt.draw()
        plt.pause(0.001)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\maxw\\PycharmProjects\\4I15 MRS Robocity\\ffmpeg-4.4' \
                                            r'-full_build\\bin\\ffmpeg.exe '
    # render = ani.save("animation%s.mp4" % timestr, fps=150, progress_callback=progress_bar)

    plt.tight_layout()
    plt.show()
