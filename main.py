from world import World
from robot_config import Robot
from routing_algorithm import route, route_multiple
from animate_robots import animate_robots
import ffmpeg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

import time

number_of_robots = 10

"""
routing_mode options:
"random"
"random_multiple"
"hungarian"
"linear_separate_tasks"
"linear_joined_tasks"
"tsm"
"home"
"""

routing_mode = "hungarian"
number_of_runs = 200


# time-step for euler integration plotting
dt = 20

if __name__ == "__main__":
    # Initialize the world

    print("\n\t Running in", routing_mode, "routing mode with", number_of_robots, "robots.")

    print("\n\t Initialising world...")
    world = World(number_of_hospitals=15, max_demand=3)

    # Initialize the robots in random warehouses
    robots = []

    print("\n\t World created. Assigning robots to warehouses...\n")

    for i in range(number_of_robots):
        warehouse = np.random.choice(world.warehouses)
        pointer = world.graph.nodes[warehouse]
        position = np.array([pointer['x'], pointer['y']])
        if i > number_of_robots/2 - 1:
            robot_type = 1
        else:
            robot_type = 0
        robot = Robot(position, i, robot_type=robot_type)
        robot._start_node = warehouse
        robots.append(robot)
        print("Robot", i, "assigned to warehouse", warehouse)

    print("\n\t Robots assigned.")

    # Invoke the routing algorithm
    print("\n\t Routing robots...")
    timer_start = time.time()
    if routing_mode == "random_multiple":
        assignment_cost = route_multiple(world, robots, mode="random", number_of_runs=number_of_runs)
    else:
        assignment_cost = route(world, robots, mode=routing_mode)[1]
    timer_end = time.time()

    computation_time = timer_end - timer_start

    # Plot everything and save animation
    print("\n\t Plotting graphs...")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('black')
    world.plot(ax=ax, show=False)
    print("\n\t Calculating animation...")

    ani = animate_robots(world, robots, fig, ax, dt)
    ax.legend()

    plt.annotate("Routing method: %s" % routing_mode, xy=(0.05, 0.95), xycoords='axes fraction',
                 backgroundcolor='white')
    plt.annotate("Makespan: %.2f s" % assignment_cost, xy=(0.05, 0.90), xycoords='axes fraction',
                 backgroundcolor='white')
    plt.annotate("Computation time: %.2f ms" % (computation_time*1000), xy=(0.05, 0.85), xycoords='axes fraction',
                 backgroundcolor='white')

    plt.tight_layout()

    print("\n\t Robots routed with assignment_cost of:", assignment_cost)
    print("\n\t Robots routed with total computation time of:", computation_time)

    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\maxw\\PycharmProjects\\4I15 MRS Robocity\\ffmpeg-4.4' \
                                            r'-full_build\\bin\\ffmpeg.exe '

    #render = ani.save("animation%s.mp4" % timestr, fps=150, progress_callback=progress_bar)

    plt.show()

