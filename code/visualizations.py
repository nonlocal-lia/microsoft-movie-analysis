# visualization packages
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
import matplotlib.ticker as mticker
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

def ticks_to_money(x, pos):
    """
    Turns int ticks to strings, prefixes a '$' and suffixes a 'M'

    Arg:
        x(int): ticklabel from matplotlib in int
        pos(int): position of tick

    Return
        str_x(str): string with $ prefixed and M as a suffixed
    """
    str_x = str(x)
    if str_x.endswith('.0'):
        str_x = str_x.replace('.0', '')
    return '$' + str_x + 'M'

def plot_top_ten(df, column_name, y_label, save_name):
    """
    Constructs barplot of the top 10 values for the input column with the input y label,
    a title incorperating that y label and an x axis labeled "Profit in Millions of Dollars"

    Arg:
        df(pdDataFrame): the df with mean and std profit values to plot
        column_name(str): the column name you will to sort by to determine the top 10
        y_label(str): a y label for the plot, which will also be used in the title
        save_name(str): a string serving as a label for the saved plot
    
    Return:
        save_name.png: a image of the plot saved to the /images/ folder
        output_plot: a barplot of the top 10 values for the input column with the input y label
    """
    c = ['c', 'm']
    output_plot = df.sort_values(by=column_name).tail(10).plot.barh(color=c)
    output_plot.set(xlabel="Profit in Millions of Dollars", ylabel=y_label,
                    title="Mean and Std of Profit by {}".format(y_label))
    if 'Std of Profit' in df.columns:
        output_plot.legend(['Average', 'Risk (std)'])
    else:
        output_plot.legend(['Average', 'Total'])
    output_plot.xaxis.set_major_formatter(mticker.FuncFormatter(ticks_to_money))
    plt.savefig(f'images/{save_name}.png')
    return output_plot

def month_plot(df,save_name):
    """
    Constructs a barplot of the values in the table by month with months labels with abrivations

    Arg:
        df(pdDataFrame): the df with month in int and mean and std profit values to plot
        save_name(str): a string serving as a label for the saved plot

    Return:
        save_name.png: a image of the plot saved to the /images/ folder
        release_plot: a barplot of the values in the table by month with months labels with abrivations
    """
    c = ['m', 'c']
    release_plot = df.plot.bar(color=c)
    release_plot.set(xlabel="Months", ylabel="Mean Profit in Millions",
                     title="Mean and Std of Profit by Release Month")
    xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    release_plot.set_xticklabels(xlabels, rotation=0)
    release_plot.legend(['Risk (std)', 'Average'])
    release_plot.yaxis.set_major_formatter(mticker.FuncFormatter(ticks_to_money))
    plt.savefig(f'images/{save_name}.png')
    return release_plot
