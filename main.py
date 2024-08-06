from ao3_plotters import *
from ao3_project_analysis import *
import pandas as pd
from conll_df import conll_df

path = 'tokenized_data/40561_tok.json'
pd.set_option('display.max_columns', None)

df = create_table_v2(path)

#df_filter = df.loc[df['upos'] == 'AUX']

#print(df_filter)

print(df)
