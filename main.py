from ao3_plotters import *
from ao3_project_analysis import *
from ao3_table_utils import *
import pandas as pd
from conll_df import conll_df

directory = 'cleaned_data'
path = 'tokenized_data/40561_tok.json'
# path = 'tokenized_data/40561_tok.conll'

freq_list_path = 'CODA_FrequencyLists/1 lemmas-Tabelle 1.csv'

pd.set_option('display.max_columns', None)

### START PROJECT ANALYSIS TEST

df = create_table_v2(path)

# df = create_table_only_words(df)

# upos_frequency(df, abs_plot=True, rel_plot=True)
# type_frequency(df, plot=True)
# res = lemma_upos_combo(df)
# res = vocabulary_growth(df, plot=True, mode='ttr')
# res = honore_h_windows(df, window_size=500)
# res = sentence_length(df)
# res = lex_density(df)

# freq_df = create_freq_df(freq_list_path)
# res = analyze_complexity(df, freq_df)
#
# print(res)

### END PROJECT ANALYSIS TEST


### START TABLE UTILS TEST

# #USED TO CREATE MASTER TABLE, ONLY EXECUTE AGAIN TO REDO FROM SCRATCH
# create_masterTable('cleaned_data')

# df = load_masterTable()
# df = masterTable_contents_by_rating(['Mature', 'Not Rated'])
#
# print (df)

### END TABLE UTILS TEST


#################
### MAIN CODE ###
#################




