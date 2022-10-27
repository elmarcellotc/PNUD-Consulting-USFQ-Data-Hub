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

from train_set_generator import get_tokenized

# Importin data

sdg = pd.read_excel('ssdg.xlsx', sheet_name = 'Sheet1', index_col=0)

# Selecting text data:

sdg['text'] = sdg['sdg'] + ' ' + sdg['ssdg']
sdg = get_tokenized(sdg)

print(sdg.head())

sdg.to_csv('sdg.csv')