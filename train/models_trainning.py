# Marcello Coletti; +593939076444 coletti.marcello@gmail.com
# USFQ Data Hub; usfqdata@gmail.com

################
# DESCRIPTION: #
################


#  This programm train the models used in text simmilarity file. Depend on the model used, it is necessary to use some or other parammeter
# type. The current folder will save the obtain params for each model, and every one will be saved on a json file.

# Library importing

import pandas as pd
import datetime

from text_similarity import jaccard


def jaccard_minimize(df_rows, df_columns, column_text, χ):
    
    columns_list = df_columns[column_text].to_list()
    columns_name = df_columns.index.to_list()
    index_list = df_rows[column_text].to_list()
    
    sim_dict = {}
    
    for i in range(len(columns_list)):
        
        sim_list = [None] * len(index_list)
        a = columns_list[i].split(' ')
        
        for j in range(len(index_list)):
            
            t1 = datetime.datetime.now()
            
            b = index_list[j].split(' ')
            
            sim_list[j] = jaccard(a, b, χ)
            
        sim_dict[columns_name[i]] = sim_list
        
    similarity = pd.DataFrame(data = sim_dict , index=df_rows.index, columns=columns_name)
    
    # Min error
    
    v = 0
    
    for i in similarity.index:
        for j in similarity.columns:                
            
            if similarity[j][i] != df_rows[j][i]:
                
                v+=1
                
    if v < ϵ:
        ϵ = v
        best_χ = χ
        
    return best_χ

def general_train(df_columns, df_rows, column_text):
        
    Α = list(range(40,61))
    
    # Future required lists
    
    Χ = [None]*len(df_rows)
    train_obs = [None]*len(Α)
    test_obs = [None]*len(Α)
    train_time = [None] * len(Α)
    test_time = [None] * len(Α)
    Ε = [None] * len(Α)
    
    for α in range(len(Α)):
        
        t1 = datetime.datetime.now()
        
        N = round(len(df_rows) * (1 - (Α[α] / 100) ))
        
        train = df_rows.iloc[:N]
        train_obs[α] = len(train)
        test = df_rows.iloc[N:]
        test_obs[α] = len(test)
            
        
        # Trainning process. The idea is to find the χ value that minimize the square error
        
        Χ_row = [i/100 for i in range(40,61)]
        ϵ = 100000000000000000000000000000000000000
        best_χ = None
        
        for χ in Χ_row:
            

                
        Χ[α] = jaccard_minimize(df_rows = train, df_columns=df_columns, column_text=column_text, χ=χ)
                    
                    


# Importing Trainning set:

main_df = pd.read_csv('train.csv', index_col=0)