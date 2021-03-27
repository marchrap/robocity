import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_config import Robot

num_nodes = 10
nodes = []
num_robots = 5
robots = []
dt = 0.01
types = ["junction", "hospital", "depot"]


class cityNode:
    def __init__(self, position, nodeType, connections):
        self.position = position
        self.nodeType = nodeType
        self.connections = connections


def create_nodes():
    for i in range(num_nodes):
        position = np.zeros(2, dtype=np.float32)
        parents = []
        position[0] = np.random.randint(-200, 200) / 100
        position[1] = np.random.randint(-200, 200) / 100
        nodeType = np.random.choice(types)
        if len(nodes):
            for j in range(np.random.randint(0, len(nodes))):
                parents.append(np.random.randint(0, len(nodes)))
        nodes.append(cityNode(position, nodeType, parents))


def create_nodes_2():
    # 0
    position = np.array([0, 0])
    nodes.append(cityNode(position, 'depot', [1, 3]))

    # 1
    position = np.array([0, 1])
    nodes.append(cityNode(position, 'junction', [0, 2, 4]))
    # 2
    position = np.array([0, 2])
    nodes.append(cityNode(position, 'junction', [0, 1, 5]))
    # 3
    position = np.array([1, 0])
    nodes.append(cityNode(position, 'junction', [0, 4, 6]))
    # 4
    position = np.array([1, 1])
    nodes.append(cityNode(position, 'junction', [1, 3, 5, 7]))
    # 5
    position = np.array([1, 2])
    nodes.append(cityNode(position, 'junction', [2, 4, 8]))
    # 6
    position = np.array([2, 0])
    nodes.append(cityNode(position, 'junction', [3, 7]))
    # 7
    position = np.array([2, 1])
    nodes.append(cityNode(position, 'junction', [4, 6, 8]))

    # 8
    position = np.array([2, 2])
    nodes.append(cityNode(position, 'hospital', [5, 7]))


def init_plot():
    fig = plt.figure()
    ax = plt.axes()  # xlim=(-2, 2), ylim=(-2, 2))
    ax.set_aspect('equal')
    return fig, ax


def plot_nodes(ax):
    '''fig = plt.figure()
    ax = plt.axes()  # xlim=(-2, 2), ylim=(-2, 2))
    ax.set_aspect('equal')'''

    for node in nodes:
        if node.nodeType == "hospital":
            shape = plt.Circle(node.position, 0.1, color='red')
        if node.nodeType == "depot":
            shape = plt.Circle(node.position, 0.1, color='blue')
        if node.nodeType == "junction":
            shape = plt.Rectangle(node.position - 0.05 / 2, 0.05, 0.05, color='black')
        ax.add_patch(shape)
        for connection in node.connections:
            x = [node.position[0], nodes[connection].position[0]]
            y = [node.position[1], nodes[connection].position[1]]
            ax.plot(x, y, c='black')


def create_path(robot):
    position_list = []
    path_nodes = robot.node_path
    speed = robot.speed

    for i in range(len(path_nodes) - 1):
        # print("i: ", i)
        start_node = nodes[path_nodes[i]]
        end_node = nodes[path_nodes[i + 1]]
        # print("start_node: ", path_nodes[i], start_node.position)
        # print("end_node: ", path_nodes[i+1], end_node.position)

        difference_vector = end_node.position - start_node.position
        # print(difference_vector, np.linalg.norm(difference_vector), difference_vector / np.linalg.norm(difference_vector))

        position = start_node.position
        position_list.append(position)

        t = 0
        while not np.allclose(position, end_node.position, atol=1e-02):  # and t < 100:
            # increment position in direction towards target
            position = position + speed * dt * difference_vector / np.linalg.norm(difference_vector)
            # print(position)
            t += dt
            position_list.append(position)
        # print(position)
        # print("t: ", t)

    return position_list


def init_robots():
    for i in range(num_robots):
        for node in nodes:
            if node.nodeType == "depot":
                position = node.position
                break
            else:
                print("no depots!")
                position = np.zeros(2, dtype=np.float32)

        robot = Robot(position, i)

        # initialise a random path of connected nodes
        path = []
        if len(nodes):
            current_node = 0
            path.append(current_node)
            for j in range(10):
                new_node = np.random.choice(nodes[current_node].connections)
                path.append(new_node)
                current_node = new_node
        #print(path)
        robot._path_of_node_integers = path
        robots.append(robot)


def init_robot_paths():
    plot_paths = []
    for robot in robots:
        path = create_path(robot)
        plot_paths.append(path)
    return plot_paths

def update(i):
    #print(path)
    #circle4 = plt.Circle(path[i], 0.1, color='blue')
    for j in range(len(robot_sprites)):
        robot_sprites[j].center = plot_paths[j][i]
        print("i: %d, j: %d" % (i, j))
        print("point: ", plot_paths[j][i])


create_nodes_2()
init_robots()
plot_paths = init_robot_paths()

fig, ax, = init_plot()

circle4 = plt.Circle((0,0), 0.1, color='blue')
ax.add_patch(circle4)

robot_sprites = []
for robot in robots:
    robot_sprites.append(plt.Circle((0,0), 0.1, color='lightblue'))
for sprite in robot_sprites:
    ax.add_patch(sprite)

plot_nodes(ax)
#animate(ax)
ani = FuncAnimation(fig, update, frames=999, interval=20, blit=False)

plt.show()
