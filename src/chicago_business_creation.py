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

sns.set(style="white", context="talk")
palette = sns.color_palette(palette='Set1')

figure, axis = plt.subplots()

# create a barplot
# http://stanford.edu/~mwaskom/software/seaborn/examples/color_palettes.html
sns.barplot(x=year_range, y=new_counts, color=palette[1])
sns.barplot(x=year_range, y=old_counts, color=palette[0])

axis.set_ylabel("year")
axis.set_ylabel("business licenses")

sns.despine(bottom=True)

plt.savefig(sys.argv[-1])
