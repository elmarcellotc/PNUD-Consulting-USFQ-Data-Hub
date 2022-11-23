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

from text_similarity import similarity, jaccard

# Minimizer function

def get_error(column_vals, real_vals):
        
    ϵ = 0 # error od type classified
        
    for j in range(len(column_vals)):
        
        ϵ = real_vals[j] - column_vals[j]
        ϵ = ϵ * ϵ
            
    return ϵ
        
    

# Main function is general_train. Will return a df with the best critical value for each model, and the params if required.

def general_train(df_rows, df_columns, column_text):

    # We want to knoe how much observations are good for train and how much for testing
    
    Α = list(range(40,61))
    
    # Future required lists
    
    Χ = [[None]*len(df_columns)] * len(df_rows) # The best χ value for each class (except non classified) (or best critical value for the model)
    train_obs = [None]*len(Α) 
    test_obs = [None]*len(Α)
    train_time = [None] * len(Α)
    test_time = [None] * len(Α)
    Ε_train = [None] * len(Α) # The minimum square error in the train datframe
    Ε_test = [None] * len(Α) # The minimum square error in the train df
    
    for α in range(len(Α)):
        
        # First train the model
        
        t1 = datetime.datetime.now()
        
        # Split train dataset according to α
        
        N = round(len(df_rows) * (1 - (Α[α] / 100) ))
        
        train = df_rows.iloc[:N,:]
        train_obs[α] = len(train)
        test = df_rows.iloc[N:,:]
        test_obs[α] = len(test)
            
        
        # Trainning process. The idea is to find the χ value that minimize the square error
        
        columns_names = df_columns.index.to_list()
        
        Χ_vals = [i/100 for i in range(40,101)]
        ϵ = [100000000000000000000000000000000000000]*len(columns_names)
        Χ_row = [None]*len(columns_names)
        
        
        
        real_values_df = train[columns_names]
        for χ in range(len(Χ_vals)):
                
            χ_list = [χ]*len(columns_names)
            similarity_df = similarity(train, df_columns, column_text, χ_list, jaccard)
            
            for i in range(len(columns_names)):
                
                column_vals = similarity_df.iloc[:,i].to_list()
                real_vals = real_values_df.iloc[:,i].to_list()
                    
                ϵ_current = get_error(column_vals, real_vals)
            
                if ϵ_current < ϵ[i]:
                    ϵ[i] = ϵ_current
                    Χ_row[i] = Χ_vals[χ]
                
        Χ[α] = Χ_row
        
        train_time[α] = datetime.datetime.now()-t1
        
        Ε_train[α] = sum(ϵ)
        
        # Now, test the model
        
        t1 = datetime.datetime.now()
        
        real_values_df = test[columns_names]
        
        similarity_df = similarity(test, df_columns, column_text, Χ_row, jaccard )
        
        ϵ = 0
        
        for i in range(len(columns_names)):
            
            column_vals = similarity_df.iloc[:,i].to_list()
            real_vals = real_values_df.iloc[:,i].to_list()
                
            ϵ += get_error(column_vals, real_vals)
        
        Ε_test[α] = ϵ 
        test_time[α] = datetime.datetime.now()-t1

        print(train_obs[α], test_obs[α], train_time[α], test_time[α], Ε_train[α], Ε_test[α])
        print(Χ_row)
        
    testing_df = pd.DataFrame({
        'train observations': train_obs,
        'test observations': test_obs,
        'training time': train_time,
        'testing time': test_time,
        'Error from training': Ε_train,
        'Error from testing': Ε_test
    })
    
    treshold_dict = {}
    
    for c in range(len(columns_names)):
        
        treshold_dict[columns_names[c]] = Χ_row[c]
    
    treshold = pd.DataFrame(treshold_dict)
    
    return testing_df, treshold

# Importing Trainning set:


if __name__ == '__main__':
    main_df = pd.read_csv('train/train.csv', index_col=0)
    
    targets = pd.read_csv('clean data/targets.csv', index_col=0)
    
    column_text = 'lemmas'    
    
    testing_df, treshold = general_train(df_rows=main_df, df_columns=targets, column_text= column_text)
    testing_df.to_csv('clean data/testing_jaccard_df.csv')
    treshold.to_csv('clean data/testing_jaccard_df.csv')