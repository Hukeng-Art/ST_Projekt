import os
import json

import pandas as pd

MASTER_FILENAME = 'ao3_MasterTable.csv'


# Tabellenoperationen für Metadaten, Zugriff auf Master-Tabelle
def create_masterTable(dir_path):
    '''
    dir_path: STRING - path to directory containing json files with story data

    Create a pandas dataframe based on data in a given directory
    Save dataframe as MASTER_FILENAME
    '''

    if not os.path.isdir(dir_path):
        print("Supplied path is not a directory!")
        return None

    files = os.listdir(dir_path)

    df_contents = []

    for file in files:
        with open(f"{dir_path}/{file}") as f:
            file_dict = json.loads(f.read())

        del file_dict['text'] # remove main text, not relevant for table focusing on everything BUT the text

        df_contents.append(file_dict)

    df = pd.DataFrame(df_contents)

    df.to_csv(MASTER_FILENAME)

def load_mastertable():
    '''
    Return PD Dataframe Object containing all metadata saved in master table (loaded from csv)
    '''

    df = pd.read_csv(MASTER_FILENAME)

    del df["Unnamed: 0"] # inelegant and probably unstable, but whatevs

    # convert string values in numeric cols to numbers
    numeric_cols = ['words', 'comments', 'kudos', 'bookmarks', 'hits', 'standardised_ttr_1000', 'standardised_ttr_500','standardised_ttr_250']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col])

    return df


def mastertable_contents_by_rating(ratings):
    '''
    rating: LIST of STRINGS - valid elements are "Not Rated", "General Audiences", "Teen And Up Audiences", "Mature", "Explicit"

    Return table only containing data for stories with the respective ratings
    NOTE: 'index' column in output table refers to index in master table
    '''

    df = load_masterTable()
    output = df[(df.rating.isin(ratings))]

    return output.reset_index()




