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

def jaccard(a, b, χ):
    
    # Jaccard Simmilarity returns the intersection of two sets divided by the union of them.            

    A = set(a)
    B = set(b)
    
    if len(A.intersection(B)) / len(A.union(B)) >= χ:
    
        return 1
    
    else:
        
        return 0
    
    return len(A.intersection(B)) / len(A.union(B))

def similarity(df_rows, df_columns, column_text, Χ = None, model=jaccard):
    
    if Χ == None:
        Χ = [0.75]*len(df_columns.index)
    
    # New columns must be the index of dfb
    
    # a_index: index or simmilarity matirx rows
    # b_index: Output and simmilarity matirx columns
    
    # This function uses one of the previous simmilarity models to get the simmilarity
    # between two text
    
    # Create a column to contrast Simmilarity
    
    columns_lemma = df_columns[column_text].to_list()
    columns_name = df_columns.index.to_list()
    index_list = df_rows[column_text].to_list()
    
    similarity_df = pd.DataFrame(index=df_rows.index, columns=columns_name)
    
    for i in range(len(columns_name)):
        
        sim_list = [None] * len(index_list)
        a = eval(columns_lemma[i])
        
        for j in range(len(index_list)):
            
            b = eval(index_list[j])
            
            sim_list[j] = model(a, b, Χ[i])

            
        similarity_df.iloc[:,i] = sim_list
    
    non_classified = [0.0]*len(sim_list)
    
    for j in range(len(similarity_df.index.to_list())):
        
        k = similarity_df.iloc[j].to_list()
        
        if k ==0:
            non_classified[j] = 1
    
    similarity_df = similarity_df.assign(target_non_classified=non_classified)

    similarity_df.loc[:, i+1] = non_classified
    
    return similarity_df


def get_amounts(similarity_df, PAI, general_sdg):
    
    # This function is to sum the amount of the flow investment according to the similarity classification
    
    amount_cols = []
    amount_dict = {}
    
    amount_dict['sdg'] = general_sdg['sdg'].tolist()
    amount_dict['sdg_information'] = general_sdg['sdg_information'].tolist()
    amount_dict['target_information'] = general_sdg['target_information'].tolist()
    
    
    for val in PAI.columns.tolist():
        if val not in ['proyecto',	'entidad',	'sectorial', 'text']:
            amount_cols.append(val)
    
    sdg_list = general_sdg.index.tolist()
    project_list = PAI.index.tolist()
    
    for val in amount_cols:
        
        amount_list = [0.0]*len(sdg_list)
        
        for s in range(len(sdg_list)):
            
            project_dict = similarity_df[sdg_list[s]].to_dict()
            pai_dict = PAI[val].to_dict()
            
            for p in project_list:
                
                if project_dict[p] == 1:
                    
                    amount_list[s] += pai_dict[p]
                    
        amount_dict[val] = amount_list
        
                
    return pd.DataFrame(data=amount_dict, index=sdg_list)
            

if __name__ == '__main__':
    
    general_sdg = pd.read_csv('raw data/targets.csv', index_col=0)
    PAI = pd.read_csv('clean data/PAI.csv', index_col=0)
    targets = pd.read_csv('clean data/targets.csv', index_col=0)
    
    column_text = 'lemmas'    
    treshold = pd.read_csv('clean data/treshold.csv')
    similarity_df = similarity(PAI, targets, column_text, treshold.iloc[0].to_list())
    similarity_df.to_csv('clean data/similarity_df.csv')
    
    
    sdg_flows = get_amounts(similarity_df, PAI, general_sdg)
    sdg_flows.to_excel('output/sdg_public_flow.xlsx')
    print(sdg_flows.head())