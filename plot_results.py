from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":


    with open('results20210413-181421.txt', 'r') as filehandle:
        results = []
        for line in filehandle:
            result = []
            # remove linebreak which is the last character of the string
            line = line[:-1]
            line_list = line.split('\t')
            if line_list[0] == "routing_mode":
                np.append(results, [line_list])
                continue

            # depreciated method
            #result.append(line_list[0])             # routing_mode
            #result.append(float(line_list[1]))        # number of robot 0
            #result.append(float(line_list[2]))        # number of robot 1
            #result.append(float(line_list[3]))        # number of robot 2
            #result.append(float(line_list[4]))      # assignment_cost
            #result.append(float(line_list[5]))      # computation_time
            #result.append(float(line_list[6]))      # total_speed_capacity

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
    results_array = np.array([xi+[None]*(length-len(xi)) for xi in results])

    print(results)
    print(results_array)

    random_makespans = []
    random_multiple_makespans =[]
    hungarian_makespans = []
    linear_separate_tasks_makespans =[]
    linear_joined_tasks_makespans = []
    tsm_makespans = []
    home_makespans = []

    for result in results:
        print(result)
        print(result[0])
        if result[0] == "random":
            random_makespans.append(result[4])
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

    fig, ax = plt.subplots()

    plt.plot(random_makespans, label="random")
    plt.plot(random_multiple_makespans, label="random_multiple")
    plt.plot(hungarian_makespans, label="hungarian")
    plt.plot(linear_separate_tasks_makespans, label="linear_separate_tasks")
    plt.plot(linear_joined_tasks_makespans, label="linear_joined_tasks")
    plt.plot(tsm_makespans, label="tsm")
    plt.plot(home_makespans, label="home")

    plt.xlabel("Ratio of robot type type1:type2")
    plt.ylabel("Makespan (s)")
    plt.legend()
    plt.show()