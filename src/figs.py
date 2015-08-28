import seaborn as sns
import matplotlib.pyplot as plt


class FlowOverTime(object):

    def __init__(self, year_range, new_counts, old_counts):

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
        axis.plot(year_range, diff_counts, color='black', linewidth=2, label='change')

        # specify the domain
        axis.axis([year_range[0]-1, year_range[-1]+1, -15000, 15000])
        axis.set_autoscale_on(False)

        # labels
        axis.legend()
        # axis.set_xlabel("year")
        axis.set_ylabel("business licenses")

        # remove crud on axes
        sns.despine(bottom=True)

    def save(self, filename):
        plt.savefig(filename)
