import random

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd

sns.set_theme(style='ticks', palette='pastel')

test_df = pd.DataFrame(
    {'category_x' : [random.randint(1,4) for i in range(128)],
     'category_hue' : [random.randint(1,5) for i in range(128)],
     'value' : [random.randint(0,32) for i in range(128)]}
)

# print(test_df)

def combined_boxplot(df, x_name, y_name, hue_name):
    '''
    turn dataframe into grouped box plot
    x_name : name (and Pd column key) for x-value
    y_name : name (and PD column key) for y-value, also dertermines number of groups
    hue_name: name (and PD column key) for value determining placement of value within subgroup
    '''
    sns.boxplot(x=x_name, y=y_name, hue=hue_name, data=df)
    matplotlib.pyplot.show()


# combined_boxplot(test_df, 'category_x', 'value', 'category_hue')
    
    