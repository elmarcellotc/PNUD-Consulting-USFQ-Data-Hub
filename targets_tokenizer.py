# Marcello Coletti; +593939076444 coletti.marcello@gmail.com
# USFQ Data Hub; usfqdata@gmail.com

##############
# DESCRIPTION:
##############

# This code is to classify the words of the sustaintable development goals as verbs, adjectives, and nouns, and
# and count the amount of every one of them.

# Importing data:

import pandas as pd
pd.options.mode.chained_assignment = None

from tokenizer import get_tokenized

# Importin data

sdg = pd.read_excel('sdg.xlsx', sheet_name = 'Sheet1', index_col=0)

# Selecting text data:

text_column = 'text'
sdg[text_column] = sdg['sdg'] + ' ' + sdg['target']
sdg = get_tokenized(sdg, text_column)

print(sdg.head())

sdg.to_csv('sdg_tokenized.csv')