from ao3_plotters import *
from ao3_project_analysis import *
from ao3_table_utils import *
import pandas as pd
from conll_df import conll_df

directory = 'cleaned_data'
path = 'tokenized_data/40561_tok.json'
# path = 'tokenized_data/40561_tok.conll'

pd.set_option('display.max_columns', None)

#df = create_table_v2(path)

# df = create_table_only_words(df)

# upos_frequency(df, abs_plot=True, rel_plot=True)
# type_frequency(df, plot=True)


#df = lemma_upos_combo(df) # CURRENT DEBUG WIP

# ### USED TO CREATE MASTER TABLE, ONLY EXECUTE AGAIN TO REDO FROM SCRATCH
# create_masterTable('cleaned_data')

df = load_masterTable()
df = masterTable_contents_by_rating(['Mature', 'Not Rated'])

print(df)


