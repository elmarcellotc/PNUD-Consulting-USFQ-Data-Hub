# Marcello Coletti; +593939076444 coletti.marcello@gmail.com
# USFQ Data Hub; usfqdata@gmail.com

##############
# DESCRIPTION:
##############

# This code uses some simmilarity functions to classify a string into one of other list of strings

# Important:

# Two elements of a sets are equal if they are equal classifyed by its word type.
# The classifications are: nouns (NN), verbs (VBP), and adjectives (JJ).

# as and bs are pandas series of the sets required to work with the simmilarity models

# Library importing

import pandas as pd

def jaccard(dfa, dfb, a, b):
    
    # Jaccard Simmilarity returns the intersection of two sets divided by the union of them.

    for j in dfb.index:
        bset = set(dfb[b][j])
        dfa[j] = None
        
        for i in dfa.index:
            aset = set(dfa[a][i])
            
            dfa[j][i] = len(aset.intersection(bset)) / len(aset.union(bset))
            

    return dfa


def simmilarity(dfa, dfb, a, b, model=jaccard):
    
    
    # New columns must be the index of dfb
    
    # a: Name of the text column in data frame dfa
    # b: Name of the text column in data frame dfb
    
    # This function uses one of the previous simmilarity models to get the simmilarity
    # between two text
    
    # Create a column to contrast Simmilarity
    
    dfa = model(dfa, dfb, a, b)
    
    dfa['sdg'] = None
    
    k = 0
    
    for j in dfb.index:
        
        for i in dfa.index:
            
            if k > dfa[j][i]:
            
                dfa['sdg'][i] = dfb['sdg'][j]
                k = dfa[j][i]
    
    dfc = dfa.groupby(by=['sdg']).sum()
    
    return dfc
    
if __name__ == '__main__':
    
    pai = pd.read_csv('pai_tokenized.csv')
    sdg = pd.read_csv('sdg_tokenized.csv')
    
    
    investment_flow = simmilarity(dfa=pai, dfb=sdg, a='tokenized', b='tokenized')
    print(investment_flow.head())
    investment_flow.to_excel('sdg_investment_flow.xlsx')