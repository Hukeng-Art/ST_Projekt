import pandas as pd
import plotly.graph_objects as go
import statistics as stats
import numpy as np
import json
from conll_df import conll_df

########

# VORSICHT – ALLES UNGETESTET!

# WAS SONST NOCH FEHLT: 
# – CODE FÜR VOKABULARSCHWIERIGKEIT
# - CODE ZUM VERGLEICH DER ERGEBNISSE 

########


# Hilfsfunktionen

def is_tsv_file(file_path):
    return file_path.endswith(".tsv")

def is_conll_file(file_path):
    return file_path.endswith(".conll")

def is_json_file(file_path):
    return file_path.endswith(".json")

# Basis: Erstelle Pandas-Tabelle
def create_table_v1(file_path):

    if is_conll_file(file_path):
        # Definiere Spaltennamen
        colnames = ['id', 'token', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']

        # Erstelle leere Liste zum Speichern der Daten
        data = []

        # Lese Datei zeilenweise ein
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Überspringe Kommentare und leere Zeilen
                if line.startswith('#') or line.strip() == '':
                    continue
                # Füge Zeile zur Datenliste hinzu
                data.append(line.strip().split('\t'))

        # Erstelle Pandas DataFrame aus den gelesenen Daten
        table = pd.DataFrame(data, columns=colnames, quoting=3)

        return table
    
    elif is_tsv_file(file_path):

        # Definiere Spaltennamen
        colnames = ['id', 'token', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']
        
        # Erstelle Pandas Dataframe
        # - quoting=3 – Anführungszeichen nicht als Quote Characters interpretieren
        # - keep_default_na=False – null nicht als NaN einlesen

        table = pd.read_table(file_path, names=colnames, quoting=3, keep_default_na=False)

        return table

# Alternativ: Erstelle Pandas-Tabelle aus json-Datei oder CONLL-Datei (unter Verwendung der conll-df library)
# Vorschlag: mit create_table_v1 verschmelzen?
def create_table_v2(file_path):
    if is_conll_file(file_path):
        df = conll_df(file_path, file_index=False, categories=True)

        # remove multi-index (makes navigation a living hell)
        df.reset_index(inplace=True)

        # change column names from random letters to correct terminology
        df.rename(columns={'s' : 'sentence',
                           'i' : 'id',
                           'w': 'token',
                           'l': 'lemma',
                           'x': 'upos',
                           'p': 'xpos',
                           'g': 'head',
                           'f': 'deprel'}, inplace=True)

        # WIP: remove rows with 'x-y' style index maybe?
        return df

    if is_json_file(file_path): # WIP

        with open(file_path) as f:
            json_data = json.loads(f.read())

        colnames = ["deprel", "end_char", "feats", "head", "id", "lemma", "misc", "multi_ner", "ner", "start_char", "text", "upos", "xpos"]

        df_data = []
        sentence_counter = 0

        for sentence in json_data:
            sentence_counter += 1
            for word in sentence:
                word_data = []

                for colname in colnames:

                    try:
                        word_data.append(word[colname])
                    except KeyError:
                        word_data.append(None)

                word_data.append(sentence_counter)

                df_data.append(word_data)

        colnames.append("sentence")
        colnames[10] = "token"

        df = pd.DataFrame(df_data, columns=colnames)

        return df

    return None



        # return pd.DataFrame([data_dict])

# Erstelle Tabelle ohne Satzzeichen (für Type Token Ratio)
def create_table_only_words(table):

    only_words_table = table.query('upos != "PUNCT"')

    # New version, compatible with create_table_v2 dfs
    # 'apply' method takes function (with row as first arg) as its first argument and applies it to each row
    # lambda function takes row as arg, returns merged string of 'token' and 'upos' col values
    only_words_table["token_upos"] = only_words_table.apply(lambda row: f"{row['token'].lower()}/{row['upos']}", axis=1)

    only_words_table = only_words_table.reset_index(drop=True) # reset indices after removing PUNCT

    return only_words_table


########

# Erste Analyse

# UPOS (Universal POS (Part of Speech)) Frequency ermitteln, also Wortartenhäufigkeit
def upos_frequency(table, abs_plot=False, rel_plot=False):

    # Tabelle erstellen mit UPOS, sowie der jeweiligen absoluten und relativen Häufigkeit
    upos_freq = table['upos'].value_counts()
    upos_freq = upos_freq.to_frame()
    upos_freq = upos_freq.reset_index()
    upos_freq.columns = ['upos', 'count']
    upos_freq = upos_freq.assign(rel=upos_freq['count'] / len(table))

    if abs_plot == True:

        # Bar-Plot zur Darstellung der absoluten Häufigkeit der unterschiedlichen Wortarten
        fig = go.Figure(data=go.Bar(x=upos_freq['upos'], y=upos_freq['count']))
        fig.update_layout(
            title="Wortartenhäufigkeiten",
            xaxis_title="UPOS-Tag",
            yaxis_title="Absolute Häufigkeit",
            template="ggplot2"
        )
        fig.show()
    
    if rel_plot == True:

        # Bar-Plot zur Darstellung der relativen Häufigkeit der unterschiedlichen Wortarten
        fig = go.Figure(data=go.Bar(x=upos_freq['upos'], y=100*upos_freq['rel']))
        fig.update_layout(
            title="Wortartenhäufigkeiten",
            xaxis_title="UPOS-Tag",
            yaxis_title="Relative Häufigkeit (in Prozent)",
            template="ggplot2"
        )
        fig.show()
    
# Type Frequency ermitteln, Häufigkeit einzelner Wörter (Types)
def type_frequency(table, plot=False):

    type_freq = table['token'].str.lower().value_counts() # bei englischen Daten lohnt es sich u.U., alle Tokens in Kleinschreibung zu berücksichtigen
    
    # Erstelle Dataframe für Type-Analyse mit Spalten für den Typen sowie die jeweilige absolute und relative Häufigkeit
    type_freq = type_freq.to_frame()
    type_freq = type_freq.reset_index()
    type_freq.columns = ['type', 'count']
    type_freq = type_freq.assign(rel=type_freq['count'] / len(table))

    print("Typen tags – absolute und relative Häufigkeit")
    print(type_freq)
    
    # Optional: Erstelle Bar-Plot mit der absoluten Häufigkeit von Tokens
    if plot == True:

        type_freq_50 = type_freq.iloc[0:50]
        fig = go.Figure(data=go.Bar(x=type_freq_50['type'], y=type_freq_50['count']))

        fig.update_layout(
            title="Verteilung der 50 häufigsten Wörter",
            xaxis_title="Type",
            yaxis_title="Absolute Häufigkeit",
            template="ggplot2"
        )

        fig.show()
    
    return type_freq

# Lemma/POS Kombinationen, Häufigkeit, Als welche Wortart treten unterschiedliche Lemmata auf?
def lemma_upos_combo(table, plot=False):

    # Neue Tabelle mit Lemma/POS Kombinationen und ihrer jeweiligen absoluten und relativen Häufigkeit
    combo_freq = (table['lemma'].str.lower() + "/" + table['upos']).value_counts()
    combo_freq = combo_freq.to_frame()
    combo_freq = combo_freq.reset_index()
    combo_freq.columns = ['lemma/upos combo', 'count']
    combo_freq = combo_freq.assign(rel=combo_freq['count'] / len(table))

    if plot == True:
        # Plot zur Visualisierung der 50 häufigsten Lemma/POS-Kombinationen
        combo_freq = combo_freq.iloc[0:50]
        fig = go.Figure(data=go.Bar(x=combo_freq['type'], y=combo_freq['count']))
        fig.update_layout(
            title="Verteilung der 50 häufigsten Lemma/POS-Kombinationen",
            xaxis_title="Type",
            yaxis_title="Absolute Häufigkeit",
            template="ggplot2"
        )
        fig.show()
    
    return combo_freq



########

# I. Säule: Umfang und Vielfältigkeit des Vokabulars


# I.1 Type Token Ratio

# Type Token Ratio, Verhältnis von Typen und Tokens 
# Hier gilt: Je größer der Wert, desto komplexer das Vokabular

# Hilfsfunktion
def ttr(n_types, n_tokens):
    return n_types / n_tokens

# Standartisiertes Type Token Ratio
# Da das Type Token Ratio von der Textlänge abhängig ist, sollte man es für den Vergleich unterschiedlich langer Texte zunächst standartisieren
def standardised_type_token_ratio(table, window_size=1000):

    only_words_table = create_table_only_words(table)

    results = []

    # 1. Text in gleich große Abschnitte teilen
    # 2. TTR für jeden Abschnitt bestimmen 
    # 3. arithmetisches Mittel aller Ergebnisse zurückgeben

    # Tokens ermittelns
    tokens = only_words_table['token_upos']   

    for i in range(int(len(tokens) / window_size)): 
        window_tokens = tokens[i*window_size:i*window_size + window_size]
        window_types = len(set(window_tokens))

        ratio = ttr(window_types, window_tokens)
        results.append(ratio)

    mean_result = stats.mean(results)
    return mean_result

# Vokabularwachstum
# je länger der Text = desto mehr unterschiedliche Wörter – aber: immer weniger neue Wörter 
def vocabulary_growth(table, mode='types', plot=False):
    
    only_words_table = create_table_only_words(table)
    tokens = only_words_table['token_upos']

    results = []
    types = set()
    for i, token in enumerate(tokens):
        types.add(token)
        if mode == 'ttr':
            results.append(ttr(len(types), i + 1))
        else:
            results.append(len(types))

    if plot == True:

        plot = go.Figure(go.Scatter(x = np.arange(1, len(results) + 1), y = results, mode='lines', name='Text 1'))
        # scatterplot.add_trace(go.Scatter(x = np.arange(1, len(vc3) + 1), y = vc3, mode='lines', name='Text 1 (BoW)'))
        plot.update_layout(
        title="Vocabulary growth curve",
        xaxis_title="Tokens",
        yaxis_title="Types")
    
        plot.show()
    
    return results



# I.2 Honorés H

# Anzahl der Wörter, die nur einmal in einem Text vorkommen (Hapax legomena), in Beziehung zur Gesamtlänge des Textes
# Hoher Wert => große Anzahl von Wörtern enthält, die nur einmal vorkommen, was auf eine hohe Wortvielfalt hinweist
def honore_h(tokens):

    n_tokens = len(tokens)
    types = tokens.value_counts()

    n_types = len(types)
    n_hapax_legomena = len(types[types == 1])
    if n_hapax_legomena == n_types:
        n_hapax_legomena -= 1 # unschöner Hack, um Divisionen durch 0 zu vermeiden
    
    result = 100 * (np.log(n_tokens) / (1 - (n_hapax_legomena / n_types)))

    return result

# Besser für Vergleichbarkeit: Einteilung in Fenster
# Generell lässt sich beobachten: je größer das Fenster/ länger der Text desto niedriger sind die Honore's H Werte
def honore_h_windows(table, window_size=1000):

    tokens = table['token_upos']

    results = []
    for i in range(int(len(tokens) / window_size)):
        window_tokens = tokens[i*window_size:i*window_size + window_size]
        results.append(honore_h(window_tokens))
    
    return np.mean(results)



########

# II. Säule: Satzkomplexität (Syntaktisch)

# Median oder Mittelwert der Satzlängen eines Texts
def mean_sentence_length(table, stat='median'):
    table['sentence'] = table.id.apply(lambda x: int(x) == 1).cumsum()
    sentence_lengths = table['sentence'].value_counts()

    if stat == 'mean':
        return stats.mean(sentence_lengths)
    else:
        return stats.median(sentence_lengths)

# Histogramm der Satzlängen
def sentence_length_histogram(table):

    table['sentence'] = table.id.apply(lambda x: int(x)==1).cumsum()
    sentence_lengths = table['sentence'].value_counts()

    fig = go.Figure(data=[go.Histogram(x=sentence_lengths)])
    fig.update_layout(
        title="Histogramm der Satzlängen",
        xaxis_title="Satzlänge",
        yaxis_title="Häufigkeit",)
    fig.show()



########

# III. Säule: Lexikalische Dichte
# Anteil der Inhaltswörter an der Gesamtzahl aller Wörter in Prozent 
# Inhaltswörter (lexical words): Wörter, die eine eigene lexikalische Bedeutung (z.B.: Adjektive, Verben, Nomen)
# vs. Funktionswörter, die überwiegend grammatikalische Bedeutung tragen (z.B.: Artikel, Konjunktionen, ...)

def lex_density(table):

    upos_freq = upos_frequency(table)

    # Inhaltswörter sammeln
    content_freq = upos_freq[upos_freq.upos.isin(['VERB', 'NOUN', 'PROPN', 'ADJ'])] # oder so: upos_freq.query("upos in ['VERB', 'NOUN', 'PROPN', 'ADJ']")
    
    # Anteil der Inhaltswörter ermitteln 
    lex_dens = content_freq['count'].sum() / upos_freq['count'].sum()

    return lex_dens



########

# IV. Vokabular-Schwierigkeit
# Vergleich mit Referenzwortliste (minimum 2000 Wörter, evtl. experimentieren)
# Option A: British National Corpus, Recherche: Wie greift man darauf zu? 
# Option B: Eigene Referenzwortliste auf Basis ALLER Fanfictions, Top 2000 Wörter, Recherche: Wie erstellen?
# Option C: Alternative suchen

# ERGÄNZEN von Code, der die Wörter in einer Table mit der gegebenen Referenzwortliste vergleicht

########

