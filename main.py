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

#df = create_table_v2(path)

# df = create_table_only_words(df)

# upos_frequency(df, abs_plot=True, rel_plot=True)
# res = type_frequency(df)
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


### START PLOTTERS TEST


test_df = pd.DataFrame(
    {'category_x' : [random.randint(1,4) for i in range(128)],
     'category_hue' : [random.randint(1,5) for i in range(128)],
     'value' : [random.randint(0,32) for i in range(128)]}
)

master_df = load_mastertable()
print(master_df)

# print(upos_freq)

# combined_boxplot(test_df, 'category_x', 'value', 'category_hue')

# bar_chart(master_df, 'title', 'standardised_ttr_500', rotate_xlabels=40, limit=25)

scatter_plot(master_df, 'standardised_ttr_500', 'standardised_ttr_250')

### END PLOTTERS TEST


#################
### MAIN CODE ###
#################

# master_df = load_masterTable()

# add standardized ttr for each text to ao3_MasterTable

# master_df['standardised_ttr_1000'] = master_df.apply(
#     lambda row : standardised_type_token_ratio(
#         create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#         window_size=1000),
#     axis=1
# )
#
# print('ws 1000 done')
#
# master_df['standardised_ttr_500'] = master_df.apply(
#     lambda row : standardised_type_token_ratio(
#         create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#         window_size=500),
#     axis=1
# )
#
# print('ws 500 done')
#
# master_df['standardised_ttr_250'] = master_df.apply(
#     lambda row : standardised_type_token_ratio(
#         create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#         window_size=250),
#     axis=1
# )
#
# print('ws 250 done')
#
# master_df.to_csv('ao3_MasterTable.csv')






