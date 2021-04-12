from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt


# define an empty list
assignment_costs = []

# open file and read the content in a list
with open('random_assignment_costs.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        assignment_costs.append(float(currentPlace))

mean_assignment_cost = sum(assignment_costs) / len(assignment_costs)

fig, axs = plt.subplots()
N, bins, patches = axs.hist(assignment_costs, bins=20)
# We'll color code by height, but you could use any scalar
fracs = N / N.max()
# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())
# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)
# Now we format the y-axis to display percentage
axs.yaxis.set_major_formatter(PercentFormatter(xmax=len(assignment_costs)))
axs.set_ylabel('Occurrence')
axs.set_xlabel('Makespan (s)')
plt.annotate("Mean assignment cost: %s" % round(mean_assignment_cost, 2), xy=(0.05, 0.95), xycoords='axes fraction')
assignment_cost = mean_assignment_cost

plt.show()