from world import World
from robot_config import Robot
from routing_algorithm import routing_algorithm
from animate_robots import animate_robots

import matplotlib.pyplot as plt
import numpy as np


number_of_robots = 4

if __name__ == "__main__":
    # Initialize the world
    world = World()

    # Initialize the robots in random warehouses
    robots = []
    for i in range(number_of_robots):
        warehouse = np.random.choice(world.warehouses)
        pointer = world.graph.nodes[warehouse]
        position = np.array([pointer['x'], pointer['y']])
        robots.append(Robot(position, i))

    # Invoke the routing algorithm
    routing_algorithm(world, robots, mode="random")

    # Plot everything and save animation
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    world.plot(show=False)
    ani = animate_robots(world, robots, fig, ax)
    # ani.save("animation.gif")
    plt.show()
