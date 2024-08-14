import random

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd


### definte plotter stlye
### pretty stuff goes here
sns.set_theme(style='ticks', palette='pastel')

############################
### ACTUAL PLOTTER FUNCS ###
############################


def boxplot(df, x_name, y_name, order=None, palette=None, x_label=None, y_label=None, title=None):
    '''

    display a boxplot on the basis of passed arguments

    :param df: PANDAS dataframe
    :param x_name: STRING - name of column to be plotted on x-axis (one box per distinct value in df)
    :param y_name: STRING - name of column to be plotted on y-axis
    :param order: LIST of STRINGS - order in which values derived from x-name should be presented
    :param palette: DICTIONARY - keys are STRINGS that correspond to x-label values, values are STRINGS, colour denominations
    :param x_label: STRING - label for x-axis
    :param y_label: STRING - label for y-axis
    :param title: STRING - label for graph
    :return: None
    '''

    plot = sns.boxplot(data=df, x=x_name, y=y_name, order=order, palette=palette)
    plot.set(xlabel=x_label, ylabel=y_label, title=title)

    matplotlib.pyplot.show()


def combined_boxplot(df, x_names, hue_name, order=None, palette=None, y_label=None, title=None, legend_title=None):

    # create and fill new dataframe in format suited for sns plotter function
    plottable_df = pd.DataFrame(columns=['x_name', 'y_name', 'hue_name'])

    for index, row in df.iterrows():
        for x_name in x_names:
            plottable_df.loc[len(plottable_df.index)] = [x_name, row[x_name], row[hue_name]]

    plot = sns.boxplot(data=plottable_df,
                x='x_name',
                y='y_name',
                hue='hue_name',
                hue_order=order,
                palette=palette
                )
    plot.set(ylabel=y_label, title=title)
    plot.legend(title=legend_title)

    matplotlib.pyplot.show()


def bar_chart(df, x_name, y_name, x_label='x_label', y_label='y_label', title='title', rotate_xlabels=0, limit=50):
    '''
    Display a seaborn bar chart based on values in passed data frame

    df : PANDAS dataframe
    x_name : STRING - name of column carrying x-axis information within df
    y_name : STRING - name of column carrying y-axis information within df
    x_label : STRING - label of x-axis
    y_label : STRING - label of y-axis
    title : STRING - label of plot
    rotate_labels: INTEGER - rotate labels by degrees, for legibility if values overlap
    limit : INTEGER - maximum number of cols
    '''

    # remove tail of dataframe
    truncated_df = df.iloc[0:limit]

    # create plot
    chart = sns.barplot(data=truncated_df, x=x_name, y=y_name)

    # set labels
    chart.set_title(title)
    chart.set_xlabel(x_label)
    chart.set_ylabel(y_label)

    # rotate x-axis labels to prevent overlap
    chart.set_xticklabels(chart.get_xticklabels(), rotation=rotate_xlabels, ha="right")

    plt.show()

def scatter_plot(df, x_name, y_name, x_label='x_label', y_label='y_label', title='title'):
    '''
    display a bi-axial (no hue) scatter plot based on values passed dataframe

    df : PANDAS dataframe
    x_name : STRING - name of column carrying x-axis information within df
    y_name : STRING - name of column carrying y-axis information within df
    x_label : STRING - label of x-axis
    y_label : STRING - label of y-axis
    title : STRING - label of plot
    '''

    # create plot
    chart = sns.scatterplot(data=df, x=x_name, y=y_name)

    # set labels
    chart.set_title(title)
    chart.set_xlabel(x_label)
    chart.set_ylabel(y_label)

    plt.show()
    pass

def scatter_plot_grid(df):
    pass
    
    