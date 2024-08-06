from ao3_plotters import *
from ao3_project_analysis import *
import pandas as pd
from conll_df import conll_df

path = 'tokenized_data/40561_tok.json'
# path = 'tokenized_data/40561_tok.conll'

pd.set_option('display.max_columns', None)

df = create_table_v2(path)

# df = create_table_only_words(df)

# upos_frequency(df, abs_plot=True, rel_plot=True)
# type_frequency(df, plot=True)


df = lemma_upos_combo(df) # CURRENT DEBUG WIP


print(df)
