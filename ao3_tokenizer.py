import stanza
from stanza.utils.conll import CoNLL
import json
import os
import time

# set up stanza pipeline
config = {
    # comma-separated list of processors to use  -- REMOVE TO GET EVERYTHING
    # 'processors': 'tokenize,mwt,pos,lemma,',
    # language code for language to use in Pipeline
    'lang': 'en', # default model is combined, see https://stanfordnlp.github.io/stanza/combined_models.html
    # use pretokenized text as input, disable tokenization
    'tokenize_pretokenized': False,
    'use_gpu': True
}


nlp = stanza.Pipeline(**config) # Initialize pipeline using configuration dict

# tokenize scraped pages
files = os.listdir('cleaned_data')
file_num = len(files)
start_time = time.time()
count = 0

for file in files:
    if f'{file.split(".")[0]}_tok.json' not in os.listdir('tokenized_data'):
        with open(f'cleaned_data/{file}') as f:

            file_dict = json.loads(f.read())
            contents = file_dict['text']

            tokenized = nlp(contents)            # tokenize ao3 work
            tokenized_dict = tokenized.to_dict() # convert tokenized text to native python obj.

            # conll = stanza.utils.conll.CoNLL.convert_dict(tokenized_dict) # convert python dict to conll format obj

        with open(f"tokenized_data/{file.split('.')[0]}_tok.json", 'w') as tok: # save tokenization data as .json
            tok.write(json.dumps(tokenized_dict, sort_keys=True, indent=4))
        # with open(f"tokenized_data/{file.split('.')[0]}_tok.conll", 'w') as tok: #save tokenization data as .conll
        #     tok.write(json.dumps(conll, sort_keys=True, indent=4))

        CoNLL.write_doc2conll(tokenized, f"tokenized_data/{file.split('.')[0]}_tok.conll")

    count += 1
    print(f'tokenized {file} \t {count}/{file_num} \t total time elapsed: {(time.time() - start_time) / 60} mins')


print('done')

