from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np


robot_type_filename = "results20210413-192130.txt"
robot_number_filename = "robot_number_results20210413-234650.txt"


if __name__ == "__main__":

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

    length = max(map(len, results))

    # convert to array
    results_array = np.array([xi + [None] * (length - len(xi)) for xi in results])

    print(results)
    print(results_array)

    robot_configs = []
    random_makespans = []
    random_multiple_makespans = []
    hungarian_makespans = []
    linear_separate_tasks_makespans = []
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        print(result)
        print(result[0])
        if result[0] == "random":
            random_makespans.append(result[4])
            robot_configs.append((result[1], result[2]))
        elif result[0] == "random_multiple":
            random_multiple_makespans.append(result[4])
        elif result[0] == "hungarian":
            hungarian_makespans.append(result[4])
        elif result[0] == "linear_separate_tasks":
            linear_separate_tasks_makespans.append(result[4])
        elif result[0] == "linear_joined_tasks":
            linear_joined_tasks_makespans.append(result[4])
        elif result[0] == "tsm":
            tsm_makespans.append(result[4])
        elif result[0] == "home":
            home_makespans.append(result[4])

    print(random_makespans)

    fig1, ax1 = plt.subplots()
    x = list(zip(*robot_configs))[0]
    plt.plot(x, random_makespans, label="random")
    plt.plot(x, random_multiple_makespans, label="random_multiple")
    plt.plot(x, hungarian_makespans, label="hungarian")
    plt.plot(x, linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(x, linear_joined_tasks_makespans, label="linear_joined_tasks")
    #plt.plot(x, tsm_makespans, label="tsm")
    #plt.plot(x, home_makespans, label="home")

    plt.xlabel("Number of robots of type 1")
    plt.ylabel("Makespan (s)")
    plt.legend()

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

    # convert to array
    results_array = np.array([xi + [None] * (length - len(xi)) for xi in results])

    print(results)
    print(results_array)

    robot_numbers = []
    random_makespans = []
    random_multiple_makespans = []
    hungarian_makespans = []
    linear_separate_tasks_makespans = []
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        #print(result)
        #print(result[0])
        if result[0] == "random":
            random_makespans.append(result[5])
            robot_numbers.append(result[4])
        elif result[0] == "random_multiple":
            random_multiple_makespans.append(result[5])
        elif result[0] == "hungarian":
            hungarian_makespans.append(result[5])
        elif result[0] == "linear_separate_tasks":
            linear_separate_tasks_makespans.append(result[5])
        elif result[0] == "linear_joined_tasks":
            linear_joined_tasks_makespans.append(result[5])
        elif result[0] == "tsm":
            tsm_makespans.append(result[5])
        elif result[0] == "home":
            home_makespans.append(result[5])

    #print(random_makespans)

    fig2, ax2 = plt.subplots()
    x = robot_numbers
    y = random_makespans

    plt.plot(x, random_makespans, label="random")
    plt.plot(x, random_multiple_makespans, label="random_multiple")
    plt.plot(x, hungarian_makespans, label="hungarian")
    plt.plot(x, linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(x, linear_joined_tasks_makespans, label="linear_joined_tasks")
    #plt.plot(list(zip(*robot_configs))[0], tsm_makespans, label="tsm")
    #plt.plot(list(zip(*robot_configs))[0], home_makespans, label="home")

    plt.xlabel("Number of robots")
    plt.ylabel("Makespan (s)")
    plt.legend()

    plt.show()
