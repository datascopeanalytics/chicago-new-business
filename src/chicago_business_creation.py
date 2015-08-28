#!/usr/bin/env python

import csv
import sys

import seaborn as sns
import matplotlib.pyplot as plt

def load_counts(filename):
    counts = {}
    with open(filename) as stream:
        stream.readline()
        reader = csv.reader(stream)
        for row in reader:
            year, count = map(int, row)
            counts[year] = count
    return counts

# read in the data
new_counts = load_counts(sys.argv[1])
old_counts = load_counts(sys.argv[2])
year_range = range(2004, 2015)
new_counts = [new_counts[year] for year in year_range]
old_counts = [-old_counts[year] for year in year_range]
diff_counts = [new + old for new, old in zip(new_counts, old_counts)]

sns.set(style="white", context="talk")
palette = sns.color_palette(palette='Set1')

figure, axis = plt.subplots()

# create a barplot
bar_width = 0.8
bar_year_range = [year - bar_width/2 for year in year_range]
axis.bar(bar_year_range, new_counts, width=bar_width, color=palette[1], edgecolor=palette[1], label='new')
axis.bar(bar_year_range, old_counts, width=bar_width, color=palette[0], edgecolor=palette[0], label='expired')

# add a line for the differences
axis.plot(year_range, diff_counts, color='k', linewidth=2)

# specify the domain
axis.axis([year_range[0]-1, year_range[-1]+1, -15000, 15000])
axis.set_autoscale_on(False)

# label axes
axis.set_xlabel("year")
axis.set_ylabel("business licenses")

# remove crud on axes
sns.despine(bottom=True)

# save figure
plt.savefig(sys.argv[-1])
