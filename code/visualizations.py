# visualization packages
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.ticker import FuncFormatter
from numpy.core.numeric import outer
import seaborn as sns

# Standard data manipulation packages
import pandas as pd
import numpy as np

matplotlib_axes_logger.setLevel('ERROR')

# Set specific parameters for the visualizations
large = 32
med = 24
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (15, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def plot_top_ten(df, column_name, y_label):
    """
    Constructs barplot of the top 10 values for the input column with the input y label,
    a title incorperating that y label and an x axis labeled "Dollars in Millions"

    Arg:
        df(pdDataFrame): the df with mean and std profit values to plot
        column_name(str): the column name you will to sort by to determine the top 10
        y_label(str): a y label for the plot, which will also be used in the title
    
    Return:
        output_plot: a barplot of the top 10 values for the input column with the input y label
    """
    c = ['b', 'r']
    output_plot = df.sort_values(by=column_name).tail(10).plot.barh(color=c)
    output_plot.set(xlabel="Dollars in Millions", ylabel=y_label,
                    title="Mean and Std of Profit by {}".format(y_label))
    output_plot
    return output_plot


def month_plot(df):
    """
    Constructs a barplot of the values in the table by month with months labels with abrivations

    Arg:
        df(pdDataFrame): the df with month in int and mean and std profit values to plot

    Return:
        release_plot: a barplot of the values in the table by month with months labels with abrivations
    """
    c = ['r', 'b']
    release_plot = df.plot.bar(color=c)
    release_plot.set(xlabel="Months", ylabel="Mean Profit in Millions",
                     title="Mean and Std of Profit by Release Month")
    xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    release_plot.set_xticklabels(xlabels, rotation=0)
    return release_plot
