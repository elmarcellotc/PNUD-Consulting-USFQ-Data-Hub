# Marcello Coletti; +593939076444 coletti.marcello@gmail.com
# USFQ Data Hub; usfqdata@gmail.com

##############
# DESCRIPTION:
##############

# This code uses the current spent dataset to create a clean dataset with the required variables of the text. To clean the text, we
# need the original identification of each observation, the original name and the entity reponsable of that spent. Then, we generate
# a second column of the previous text without capital letters, accent marks, special characters, or punctuation marks.

# Importing data:

import pandas as pd
pd.options.mode.chained_assignment = None

pai = pd.read_csv('pai.csv', index_col = 0)

pai['text'] = pai['entidad'] + ' ' + pai['proyecto']

# Make text column lower case

pai['text'] = pai['text'].str.lower()

# Removing punctuation marks and special characters:
 
pai['text'] = pai['text'].str.replace('.', '', regex=True)
pai['text'] = pai['text'].str.replace(',', '', regex=True)
pai['text'] = pai['text'].str.replace(';', '', regex=True)
pai['text'] = pai['text'].str.replace(':', '', regex=True)
pai['text'] = pai['text'].str.replace('-', '', regex=True)
pai['text'] = pai['text'].str.replace('_', '', regex=True)
pai['text'] = pai['text'].str.replace('#', '', regex=True)
pai['text'] = pai['text'].str.replace('$', '', regex=True)
pai['text'] = pai['text'].str.replace('&', '', regex=True)
pai['text'] = pai['text'].str.replace('=', '', regex=True)

pai['text'] = pai['text'].str.replace('  ', ' ', regex=True)

# Removing numbers from text

pai['text'] = pai['text'].str.replace('\d+', '', regex=True)

# We don't want prepositions, conjunctions, or adverbs in our text, so we uses NTKL to identify and remove them
# See the documentation here: https://www.nltk.org/api/nltk.tokenize.html, https://www.nltk.org/api/nltk.tag.html


def clean_by_type(sentence):

    from nltk import word_tokenize  # To classify words in semantical types
    from nltk import pos_tag        # To show the previous classification

    # We are not able to work in spanish rigth now, so, we transform the sentece to english with google translate library.

    from googletrans import Translator

    translator = Translator()
    
    sentence = translator.translate(sentence, src='es', dest='en').text

    sentence = word_tokenize(sentence) 

    # We're searching for nouns (NN), verbs (VBP), and adjectives (JJ).

    sentence = pos_tag(sentence, lang = 'eng')

    sentence = [ i for i in sentence if i[1] in ['NN', 'VBP', 'JJ'] ]

    word_types = [ i[1] for i in sentence ]
    sentence = [ i[0] for i in sentence ]
    
    return sentence, word_types

# Generate columns with clean_by_type() function

pai['sentence'] = None
pai['word_types'] = None
pai['nouns'] = None
pai['verbs'] = None
pai['adjectives'] = None

for i in pai.index:
    
    pai['sentence'][i], pai['word_types'][i] = clean_by_type(pai['text'][i])
    pai['nouns'][i] = pai['word_types'][i].count('NN')
    pai['verbs'][i] = pai['word_types'][i].count('VBP')
    pai['adjectives'][i] = pai['word_types'][i].count('JJ')
    
    print(pai['sentence'][i])
    print(pai['word_types'][i])
    print(pai['nouns'][i], pai['verbs'][i], pai['adjectives'][i], '\n')
    
# Export dataframe

pai.to_csv('pai_tokenized.csv')