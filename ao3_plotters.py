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

def combined_boxplot(df, x_names, hue_name, x_label='x_label', y_label='y_label', plot_title='plot_title'):
    '''
    turn dataframe into grouped box plot
    df : PANDAS dataframe
    x_name : LIST of STRINGS - names (and PD column keys) for x-value, length determines number of groups
    hue_name: STRING - name (and PD column key) for value determining placement of value within subgroup
    '''

    # create and fill new dataframe in format suited for sns plotter function
    plottable_df = pd.DataFrame(columns=['x_name', 'y_name', 'hue_name'])

    for index, row in df.iterrows():
        for x_name in x_names:
            plottable_df.loc[len(plottable_df.index)] = [x_name, row[x_name], row[hue_name]]


    sns.boxplot(x='x_name', y='y_name', hue='hue_name', data=plottable_df)
    matplotlib.pyplot.show()


def bar_chart(df, x_name, y_name, x_label='x_label', y_label='y_label', plot_title='plot_title', rotate_xlabels=0, limit=50):
    '''
    Display a seaborn bar chart based on values in passed data frame

    df : PANDAS dataframe
    x_name : STRING - name of column carrying x-axis information within df
    y_name : STRING - name of column carrying y-axis information within df
    x_label : STRING - label of x-axis
    y_label : STRING - label of y-axis
    plot_title : STRING - label of plot
    rotate_labels: INTEGER - rotate labels by degrees, for legibility if values overlap
    limit : INTEGER - maximum number of cols
    '''

    # remove tail of dataframe
    truncated_df = df.iloc[0:limit]

    # create plot
    chart = sns.barplot(data=truncated_df, x=x_name, y=y_name)

    # set labels
    chart.set_title(plot_title)
    chart.set_xlabel(x_label)
    chart.set_ylabel(y_label)

    # rotate x-axis labels to prevent overlap
    chart.set_xticklabels(chart.get_xticklabels(), rotation=rotate_xlabels, ha="right")

    plt.show()

def scatter_plot(df, x_name, y_name, x_label='x_label', y_label='y_label', plot_title='plot_title'):
    '''
    display a bi-axial (no hue) scatter plot based on values passed dataframe

    df : PANDAS dataframe
    x_name : STRING - name of column carrying x-axis information within df
    y_name : STRING - name of column carrying y-axis information within df
    x_label : STRING - label of x-axis
    y_label : STRING - label of y-axis
    plot_title : STRING - label of plot
    '''

    # create plot
    chart = sns.scatterplot(data=df, x=x_name, y=y_name)

    # set labels
    chart.set_title(plot_title)
    chart.set_xlabel(x_label)
    chart.set_ylabel(y_label)

    plt.show()
    pass

def scatter_plot_grid(df):
    pass
    
    