from world import World
from robot_config import Robot
from routing_algorithm import routing_algorithm
from animate_robots import animate_robots

import matplotlib.pyplot as plt
import numpy as np

import time

number_of_robots = 4

routing_mode = "random"

# time-step for euler integration plotting
dt = 5

if __name__ == "__main__":
    # Initialize the world

    print("\n\t Running in", routing_mode, "routing mode with", number_of_robots, "robots.")

    print("\n\t Initialising world...")
    world = World()

    # Initialize the robots in random warehouses
    robots = []

    print("\n\t World created. Assigning robots to warehouses...\n")

    for i in range(number_of_robots):
        warehouse = np.random.choice(world.warehouses)
        pointer = world.graph.nodes[warehouse]
        position = np.array([pointer['x'], pointer['y']])
        if i > 1:
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
    assignment_cost = routing_algorithm(world, robots, mode=routing_mode)
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
    plt.annotate("Flowtime: %.2f s" % assignment_cost, xy=(0.05, 0.90), xycoords='axes fraction',
                 backgroundcolor='white')
    plt.annotate("Computation time: %.2f ms" % computation_time*1000, xy=(0.05, 0.85), xycoords='axes fraction',
                 backgroundcolor='white')


    print("\n\t Robots routed with total flowtime of:", assignment_cost)
    print("\n\t Robots routed with total computation time of:", computation_time)

    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    #ani.save("animation%s.gif" % timestr)

    plt.show()
