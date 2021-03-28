from world import World
from robot_config import Robot
from routing_algorithm import routing_algorithm
from animate_robots import animate_robots

import matplotlib.pyplot as plt
import numpy as np


number_of_robots = 6

if __name__ == "__main__":
    # Initialize the world
    print("\n\t Initialising world...")
    world = World()

    # Initialize the robots in random warehouses
    robots = []

    print("\n\t World created. Assigning robots to warehouses...\n")

    for i in range(number_of_robots):
        warehouse = np.random.choice(world.warehouses)
        pointer = world.graph.nodes[warehouse]
        position = np.array([pointer['x'], pointer['y']])
        if i > 3:
            robot_type = 1
        else:
            robot_type = 0
        robot = Robot(position, i, robot_type=robot_type)
        robot._start_node = warehouse
        robots.append(robot)
        print("Robot ", i, " to warehouse", warehouse)

    print("\n\t Robots assigned.")

    # Invoke the routing algorithm
    routing_algorithm(world, robots, mode="random")

    # # Plot everything and save animation
    # fig, ax = plt.subplots(figsize=(8, 8))
    # #ax.set_aspect('equal')
    # ax.set_facecolor('black')
    # world.plot(ax=ax, show=False)
    # ani = animate_robots(world, robots, fig, ax)
    # # ani.save("animation.gif")
    # plt.show()
