from ao3_plotters import *
from ao3_project_analysis import *
from ao3_table_utils import *
import pandas as pd
from conll_df import conll_df

directory = 'cleaned_data'
path = 'tokenized_data/40561_tok.json'
# path = 'tokenized_data/40561_tok.conll'

FREQ_LIST_PATH = 'CODA_FrequencyLists/1 lemmas-Tabelle 1.csv'

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

# freq_df = create_freq_df(FREQ_LIST_PATH)
# res = analyze_complexity(df, freq_df)
#
# print(res)

### END PROJECT ANALYSIS TEST


### START TABLE UTILS TEST

# #USED TO CREATE MASTER TABLE, ONLY EXECUTE AGAIN TO REDO FROM SCRATCH
# create_mastertable('cleaned_data')

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

# master_df = load_mastertable()
# print(master_df)

# print(upos_freq)

# combined_boxplot(test_df, 'category_x', 'value', 'category_hue')

# bar_chart(master_df, 'title', 'standardised_ttr_500', rotate_xlabels=40, limit=25)

# scatter_plot(master_df, 'standardised_ttr_500', 'standardised_ttr_250')

### END PLOTTERS TEST


#################
### MAIN CODE ###
#################

master_df = load_mastertable()

### BEGIN ADD INFO TO MASTER
#
# # add standardized ttr for each text to ao3_MasterTable, different window sizes
# for value in [250, 500, 1000, 4000]:
#     master_df[f"standardised_ttr_{value}"] = master_df.apply(
#         lambda row: standardised_type_token_ratio(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             window_size=value),
#         axis=1
#     )
#
#     print(f"ttr {value} added")
#
# # add honore h for each text to ao3_MasterTable, different window sizes
# for value in [250, 500, 1000, 4000]:
#     master_df[f"honore_h_{value}"] = master_df.apply(
#         lambda row: honore_h_windows(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             window_size=value),
#         axis=1
#     )
#
#     print(f"honore h {value} added")
#
# # add vocabulary growth ttr
# master_df["vocabulary_growth_ttr"] = master_df.apply(
#         lambda row: vocabulary_growth(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             mode="ttr"),
#         axis=1
#     )
#
# print("vocabulary growth ttr added")
#
# # add vocabulary growth types
# master_df["vocabulary_growth_types"] = master_df.apply(
#         lambda row: vocabulary_growth(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             mode="types"),
#         axis=1
#     )
#
# print("vocabulary growth types added")
#
# # add sentence length mean
# master_df["sentence_length_mean"] = master_df.apply(
#         lambda row: sentence_length(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             stat="mean"),
#         axis=1
#     )
#
# print("sentence length mean added")
#
# # add sentence length median
# master_df["sentence_length_median"] = master_df.apply(
#         lambda row: sentence_length(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             stat="median"),
#         axis=1
#     )
#
# print("sentence length median added")
#
# # add lexical density
# master_df["lexical_density"] = master_df.apply(
#         lambda row: lex_density(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json")),
#         axis=1
#     )
#
# print("lexical density added")
#
# # add lexical density
# master_df["complexity_stats"] = master_df.apply(
#         lambda row: analyze_complexity(
#             create_table_v2(f"tokenized_data/{row['id']}_tok.json"),
#             create_freq_df(FREQ_LIST_PATH)
#         ),
#         axis=1
#     )
#
# print("complexity stats added")
#
# master_df.to_csv(MASTER_FILENAME)
#
# # add complexity known word ratio as distinct col
# master_df['known_word_ratio'] = master_df.apply(lambda row: row['complexity_stats']["known_word_ratio"], axis=1)
#
# print('Added known word ratio as distinct stat')
#
# master_df.to_csv(MASTER_FILENAME)

# END ADD INFO TO MASTER


ttr_colnames = ['standardised_ttr_250', 'standardised_ttr_500', 'standardised_ttr_1000', 'standardised_ttr_4000']

print(master_df)


combined_boxplot(master_df, ttr_colnames, 'rating')




