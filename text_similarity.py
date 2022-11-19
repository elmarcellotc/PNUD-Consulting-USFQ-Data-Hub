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
import datetime
    

def jaccard(a, b):
    
    # Jaccard Simmilarity returns the intersection of two sets divided by the union of them.            

    A = set(a)
    B = set(b)
    
    return len(A.intersection(B)) / len(A.union(B))

def simmilarity(df_rows, df_columns, column_text, model=jaccard):
    
    
    # New columns must be the index of dfb
    
    # a_index: index or simmilarity matirx rows
    # b_index: Output and simmilarity matirx columns
    
    # This function uses one of the previous simmilarity models to get the simmilarity
    # between two text
    
    # Create a column to contrast Simmilarity
    
    columns_list = df_columns[column_text].to_list()
    columns_name = df_columns.index.to_list()
    index_list = df_rows[column_text].to_list()
    
    sim_dict = {}
    
    row_time = [None]*(len(columns_list) * len(index_list))
    k = 0
    
    for i in range(len(columns_list)):
        
        sim_list = [None] * len(index_list)
        a = columns_list[i].split(' ')
        
        for j in range(len(index_list)):
            
            t1 = datetime.datetime.now()
            
            b = index_list[j].split(' ')
            
            sim_list[j] = model(a, b)
            
            row_time[k] = datetime.datetime.now() - t1
            k+=1
            
        sim_dict[columns_name[i]] = sim_list
    
    return pd.DataFrame(data = sim_dict , index=df_rows.index), row_time
    
    
if __name__ == '__main__':
    
    clean_df = pd.read_csv('clean_df.csv')
    targets = pd.read_csv('targets.csv', index_col=1)
    
    column_text = 'text'    
    
    simmilarity_df, row_time = simmilarity(clean_df, targets, column_text)
    print(simmilarity_df.head())
    simmilarity_df.to_csv('simmilarity_df.csv')
    
    testing_info = pd.DataFrame()
    testing_info['duration'] = row_time
    import os
    testing_info['programm'] = os.path.basename(__file__)
    print(testing_info.head())
    testing_info.to_csv('testing_info.csv')