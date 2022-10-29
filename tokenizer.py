# Marcello Coletti; +593939076444 coletti.marcello@gmail.com
# USFQ Data Hub; usfqdata@gmail.com

##############
# DESCRIPTION:
##############

# This code uses the current spent dataset to create a clean dataset with the required variables of the text. To clean the text, we
# need the original identification of each observation, the original name and the entity reponsable of that spent. Then, we generate
# a second rowof the previous text without capital letters, accent marks, special characters, or punctuation marks.

# Main library:

import pandas as pd
pd.options.mode.chained_assignment = None


def clean_text(df, text_column):

    # Make text rowlower case

    df[text_column] = df[text_column].str.lower()

    # Removing punctuation marks and special characters:
    
    df[text_column] = df[text_column].str.replace('.', '', regex=True)
    df[text_column] = df[text_column].str.replace(',', '', regex=True)
    df[text_column] = df[text_column].str.replace(';', '', regex=True)
    df[text_column] = df[text_column].str.replace(':', '', regex=True)
    df[text_column] = df[text_column].str.replace('-', '', regex=True)
    df[text_column] = df[text_column].str.replace('_', '', regex=True)
    df[text_column] = df[text_column].str.replace('#', '', regex=True)
    df[text_column] = df[text_column].str.replace('$', '', regex=True)
    df[text_column] = df[text_column].str.replace('&', '', regex=True)
    df[text_column] = df[text_column].str.replace('=', '', regex=True)

    df[text_column] = df[text_column].str.replace('  ', ' ', regex=True)

    # Removing numbers from text

    df[text_column] = df[text_column].str.replace('\d+', '', regex=True)

    
    return df

def get_tokenized(df, text_column):
    
    df = clean_text(df, text_column )
    
    # We don't want prepositions, conjunctions, or adverbs in our text, so we uses NTKL to identify and remove them
    # See the documentation here: https://www.nltk.org/api/nltk.tokenize.html, https://www.nltk.org/api/nltk.tag.html

    from nltk import word_tokenize  # To classify words in semantical types
    from nltk import pos_tag        # To show the previous classification

    # We are not able to work in spanish rigth now, so, we transform the sentece to english with google translate library.
    
    df['tokenized'] = df.apply(
        lambda row: word_tokenize(row[text_column]), axis=1
    ) 

    # We're searching for nouns (NN), verbs (VBP), and adjectives (JJ).

    df['tokenized'] = df.apply(
        lambda row: pos_tag(row['tokenized'], lang = 'eng'), axis=1
    )
    
    df['tokenized'] = df.apply(
        lambda row: [ i for i in row['tokenized'] for j in i if j in ['NN', 'VBP', 'JJ'] ],
        axis=1
    )
    
    return df

# Generate columns with clean_by_type() function


def clean_translating(df, text_column, src='es'):

    from googletrans import Translator

    translator = Translator()

    df['sentence'] = df.apply(
        lambda row: translator.translate(row[text_column], src=src, dest='en').text ,axis=1
        )

    df = get_tokenized(df, text_column)
        
    return df

if __name__ == '__main__':

    # Import data    
    
    pai = pd.read_csv('pai.csv', index_col = 0)
    text_column = 'text'
    pai[text_column] = pai['entidad'] + ' ' + pai['proyecto']
    
    pai = clean_translating(pai, text_column)
    
    # Export dataframe

    pai.to_csv('pai_tokenized.csv')