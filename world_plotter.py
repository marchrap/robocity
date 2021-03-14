import matplotlib
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.patches.ConnectionPatch

num_nodes = 10
nodes = []
types = ["junction", "hospital", "depot"]


class node:
    def __init__(self, position, nodeType, parents):
        self._position = position
        self._type = nodeType
        self._parents = parents


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
        nodes.append(node(position, nodeType, parents))


def init_plot():
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))


def plot_nodes():
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
    ax.set_aspect('equal')

    for node in nodes:
        if node._type == "hospital":
            shape = plt.Circle(node._position, 0.1, color='red')
        if node._type == "depot":
            shape = plt.Circle(node._position, 0.1, color='blue')
        if node._type == "junction":
            shape = plt.Rectangle(node._position - 0.05, 0.05, 0.05, color='black')
        ax.add_patch(shape)
        for parent in node._parents:
            x = [node._position[0], nodes[parent]._position[0]]
            y = [node._position[1], nodes[parent]._position[1]]
            ax.plot(x, y)



create_nodes()
# init_plot()
plot_nodes()
plt.show()
