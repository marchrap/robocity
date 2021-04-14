from typing import List, Union

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np

method_comparison_filename = "method_comparison_results_final.txt"
robot_type_filename = "robot_type_results_final.txt"
robot_number_filename = "robot_number_results_final.txt"
increased_demand_filename = "increased_demand_results_final.txt"

if __name__ == "__main__":

    """
        Experiment with varying robot types.
    """

    with open(robot_type_filename, 'r') as filehandle:
        results = []
        for line in filehandle:
            result = []
            # remove linebreak which is the last character of the string
            line = line[:-1]
            line_list = line.split('\t')
            if line_list[0] == "routing_mode":
                np.append(results, [line_list])
                continue

            for string_element in line_list:
                try:
                    element = float(string_element)
                except ValueError:
                    element = string_element
                result.append(element)

            # add item to the list
            results.append(result)

    print(results)

    robot_configs = []
    random_makespans = []
    random_multiple_makespans = []
    hungarian_makespans = []
    linear_separate_tasks_makespans = []
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        # print(result)
        # print(result[0])
        if result[0] == "random":
            random_makespans.append(result[7])
            robot_configs.append((result[1], result[2]))
        elif result[0] == "random_multiple":
            random_multiple_makespans.append(result[7])
        elif result[0] == "hungarian":
            hungarian_makespans.append(result[7])
        elif result[0] == "linear_separate_tasks":
            linear_separate_tasks_makespans.append(result[7])
        elif result[0] == "linear_joined_tasks":
            linear_joined_tasks_makespans.append(result[7])
        elif result[0] == "tsm":
            tsm_makespans.append(result[7])
        elif result[0] == "home":
            home_makespans.append(result[7])

    fig1, ax1 = plt.subplots()
    x = list(zip(*robot_configs))[0]
    plt.plot(x, random_makespans, label="random")
    plt.plot(x, random_multiple_makespans, label="random_multiple")
    plt.plot(x, hungarian_makespans, label="hungarian")
    plt.plot(x, linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(x, linear_joined_tasks_makespans, label="linear_joined_tasks")
    plt.plot(x, tsm_makespans, label="tsm")
    plt.plot(x, home_makespans, label="home")

    plt.xlabel("Number of robots of type 1")
    plt.ylabel("Makespan (s)")
    plt.legend()

    """
    Now experiment with varying robot number.
    """

    with open(robot_number_filename, 'r') as filehandle:
        results = []
        for line in filehandle:
            result = []
            # remove linebreak which is the last character of the string
            line = line[:-1]
            line_list = line.split('\t')
            if line_list[0] == "routing_mode":
                np.append(results, [line_list])
                continue

            for string_element in line_list:
                try:
                    element = float(string_element)
                except ValueError:
                    element = string_element
                result.append(element)

            # add item to the list
            results.append(result)

    length = max(map(len, results))

    print(results)

    robot_numbers = []
    random_makespans = []
    random_multiple_makespans = []
    hungarian_makespans = []
    linear_separate_tasks_makespans = []
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        # print(result)
        # print(result[0])
        if result[0] == "random":
            random_makespans.append(result[7])
            robot_numbers.append(result[4])
        elif result[0] == "random_multiple":
            random_multiple_makespans.append(result[7])
        elif result[0] == "hungarian":
            hungarian_makespans.append(result[7])
        elif result[0] == "linear_separate_tasks":
            linear_separate_tasks_makespans.append(result[7])
        elif result[0] == "linear_joined_tasks":
            linear_joined_tasks_makespans.append(result[7])
        elif result[0] == "tsm":
            tsm_makespans.append(result[7])
        elif result[0] == "home":
            home_makespans.append(result[7])

    fig2, ax2 = plt.subplots()
    x = robot_numbers
    y = random_makespans

    plt.plot(x, random_makespans, label="random")
    plt.plot(x, random_multiple_makespans, label="random_multiple")
    plt.plot(x, hungarian_makespans, label="hungarian")
    plt.plot(x, linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(x, linear_joined_tasks_makespans, label="linear_joined_tasks")
    plt.plot(x, tsm_makespans, label="tsm")
    plt.plot(x, home_makespans, label="home")

    plt.xlabel("Number of robots")
    plt.ylabel("Makespan (s)")
    plt.legend()

    """
    Now increase demand.
    """

    with open(increased_demand_filename, 'r') as filehandle:
        results = []
        for line in filehandle:
            result = []
            # remove linebreak which is the last character of the string
            line = line[:-1]
            line_list = line.split('\t')
            if line_list[0] == "routing_mode":
                np.append(results, [line_list])
                continue

            for string_element in line_list:
                try:
                    element = float(string_element)
                except ValueError:
                    element = string_element
                result.append(element)

            # add item to the list
            results.append(result)

    print(results)

    max_demands = []
    random_makespans = []
    random_multiple_makespans = []
    hungarian_makespans = []
    linear_separate_tasks_makespans = []
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        # print(result)
        # print(result[0])
        if result[0] == "random":
            random_makespans.append(result[7])
            max_demands.append(result[5])
        elif result[0] == "random_multiple":
            random_multiple_makespans.append(result[7])
        elif result[0] == "hungarian":
            hungarian_makespans.append(result[7])
        elif result[0] == "linear_separate_tasks":
            linear_separate_tasks_makespans.append(result[7])
        elif result[0] == "linear_joined_tasks":
            linear_joined_tasks_makespans.append(result[7])
        elif result[0] == "tsm":
            tsm_makespans.append(result[7])
        elif result[0] == "home":
            home_makespans.append(result[7])

    fig2, ax2 = plt.subplots()
    x = max_demands
    y = random_makespans

    plt.plot(x, random_makespans, label="random")
    plt.plot(x, random_multiple_makespans, label="random_multiple")
    plt.plot(x, hungarian_makespans, label="hungarian")
    plt.plot(x, linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(x, linear_joined_tasks_makespans, label="linear_joined_tasks")
    plt.plot(x, tsm_makespans, label="tsm")
    plt.plot(x, home_makespans, label="home")

    plt.xlabel("Max demand")
    plt.ylabel("Makespan (s)")
    plt.legend()

    """
    Plot bar chart of methods on standard 15 hospital, 10 robot, world.
    """

    conlusion_results = [["Random baseline(n=2000)", 4045.34],
                         ["Hungarianish", 2421.16],
                         ["linear_separate_tasks", 2071.02],
                         ["linear_joined_tasks", 1430.11],
                         ["tsm(60s)", 2137.76],
                         ["tsm(120s)", 829.40],
                         ["home", 829.40]]

    with open(method_comparison_filename, 'r') as filehandle:
        results = []
        for line in filehandle:
            result = []
            # remove linebreak which is the last character of the string
            line = line[:-1]
            line_list = line.split('\t')
            if line_list[0] == "routing_mode":
                np.append(results, [line_list])
                continue

            for string_element in line_list:
                try:
                    element = float(string_element)
                except ValueError:
                    element = string_element
                result.append(element)

            # add item to the list
            results.append(result)

    print(results)

    makespans = []
    flowspans = []
    scores = []
    computation_times = []
    labels: List[Union[float, str]] = []

    for result in results:
        # print(result)
        # print(result[0])
        labels.append(result[0])
        makespans.append(result[7])
        flowspans.append(result[8])
        scores.append(result[9])
        computation_times.append(result[10])

    computation_times[1] /= 30

    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA

    fig3, ax3 = plt.subplots(figsize=(12, 7.5))
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(left=0.1, right=0.8, bottom=0.1, top=0.9)
    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    offset = 60

    par1.axis["right"].toggle(all=True)

    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par2.axis["right"].toggle(all=True)

    new_fixed_axis2 = par3.get_grid_helper().new_fixed_axis
    par3.axis["right"] = new_fixed_axis2(loc="right",
                                         axes=par3,
                                         offset=(offset * 2, 0))

    par3.axis["right"].toggle(all=True)

    host.set_ylabel("Makespan (s)")
    par1.set_ylabel("Flowspan (s)")
    par2.set_ylabel("Score")
    par3.set_ylabel("Computation time (s)")

    y_pos = np.arange(len(makespans) - 1)
    bar_width = 0.2
    opacity = 0.8

    # print(y_pos)
    # print(makespans)

    colours = ['b', 'g', 'r', 'y']

    rects1 = host.bar(y_pos - 1.5 * bar_width, makespans[1:], bar_width,
                      alpha=opacity,
                      color=colours[0],
                      label='Makespan (s)')

    for i, v in enumerate(makespans[1:]):
        host.text(i-bar_width*1.5, v+0.01*max(makespans[1:]), str(round(v,2)), ha='center', va='bottom', rotation=90)

    rects2 = par1.bar(y_pos - 0.5 * bar_width, flowspans[1:], bar_width,
                      alpha=opacity,
                      color=colours[1],
                      label='Flowspan (s)')

    for i, v in enumerate(flowspans[1:]):
        par1.text(i-bar_width*0.5, v+0.01*max(flowspans[1:]), str(round(v,2)), ha='center', va='bottom', rotation=90)

    rects3 = par2.bar(y_pos + 0.5 * bar_width, scores[1:], bar_width,
                      alpha=opacity,
                      color=colours[2],
                      label='Score')

    for i, v in enumerate(scores[1:]):
        par2.text(i+bar_width*0.5, v+0.01*max(scores[1:]), str(round(v,2)), ha='center', va='bottom', rotation=90)

    rects4 = par3.bar(y_pos + 1.5 * bar_width, computation_times[1:], bar_width,
                      alpha=opacity,
                      color=colours[3],
                      label='Computation time (s)')

    for i, v in enumerate(computation_times[1:]):
        par3.text(i+bar_width*1.5, v+0.01*max(computation_times[1:]), str(round(v,2)), ha='center', va='bottom', rotation=90)

    new_labels = ["random only",
                  "random average\n(n=2000)",
                  "hungarian",
                  "linear\nseparate",
                  "linear\njoined",
                  "tsm (60s)",
                  "tsm (120s)",
                  "home"]

    ax3.set_visible(False)

    host.set_xticks(y_pos)
    host.set_xticklabels([])

    for label, position in zip(new_labels[1:], y_pos):
        plt.annotate(label, (0.1+position/7.5, 0), (0, -5), xycoords='axes fraction', textcoords='offset points', va='top',
                     ha='center')


    host.legend()

    host.axis["left"].label.set_color(color=colours[0])
    par1.axis["right"].label.set_color(color=colours[1])
    par2.axis["right"].label.set_color(color=colours[2])
    par3.axis["right"].label.set_color(color=colours[3])

    par1.set_visible(False)
    par2.set_visible(False)
    par3.set_visible(False)

    # plt.tight_layout()

    # plt.draw()

plt.show()
