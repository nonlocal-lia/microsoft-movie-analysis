# visualization packages
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Standard data manipulation packages
import pandas as pd
import numpy as np

matplotlib_axes_logger.setLevel('ERROR')

# Set specific parameters for the visualizations
large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def plot_top_ten(df, column_name, y_label):
    """
    Takes in a dataframe of with two columns of stats in millions off dollars of profit,
    a column name to sort by, and a y_label for the chart,
    and returns a barplot of the top 10 values for that column
    """
    c = ['b', 'r']
    output_plot = df.sort_values(by=column_name).tail(10).plot.barh(color=c)
    output_plot.set(xlabel="Dollars in M", ylabel=y_label,
                    title="Mean and Std of Profit by {}".format(y_label))
    return output_plot


def month_plot(df):
    """
    Takes in a dataframe with months in int and matching stats about profit
    and returns a barplot of those values for each month
    """
    c = ['r', 'b']
    release_plot = df.plot.bar(color=c)
    release_plot.set(xlabel="Months", ylabel="Mean Profit in Millions",
                     title="Mean and Std of Profit by Release Month")
    xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    release_plot.set_xticklabels(xlabels, rotation=0)
    return release_plot
