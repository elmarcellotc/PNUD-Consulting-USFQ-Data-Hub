# Marcello Coletti; USFQ Data Hub
# (+593)939076444, coletti.marcellogmail.com, mcoletti@estud.usfq.edu.ec 
#

# Description: This file is made to join the data bases from the Ecuadorian Ministry of Finance "Plan de Inversiones"
# from 2017 to 2021. The data will be used to measure the flow of investment in the public sector in the Sustainable
# Development Goals of the UN.

# The files were downloaded from https://www.finanzas.gob.ec/ejecucion-presupuestaria/ >> 'Plan Anual nde Inversiones'
# in August-September 2022

# TO DO: Export aggregated file

# Libraies importing

import pandas as pd
pd.options.mode.chained_assignment = None

# The next df is a general Data Frame to reordered

PAI = pd.DataFrame()
PAI.index.names = ['id']


def cleanup(year, index_dict, project_counter):

    df = pd.read_csv(f'raw data/PLAN ANUAL DE INVERSIONES {year}.csv')
    
    colnames = df.columns.tolist()
    colnames[0] = 'sectorial'
    colnames[1] = 'entidad'
    colnames[2] = 'proyecto'
    colnames[3] = 'fuente'
    
    df1 = df.copy()
    df1.columns = colnames
    
    # This database doesn't have missing values. The Website was created to download an excel file. So, 
    # every NaN or missing value is equal to its previous value in the previous row.
    df1 = df1.fillna(method='ffill')

    # The last row shows the sumation of the vector. I drop this row now because it is not necessary for the consulting.
    df1 = df1.iloc[:-1]
    
    colnames = df1.columns.tolist()

    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
              'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    flow_type = ['C', 'D']
    flow_original = ['Codificado', 'Devengado']

    # The new way of the datetime is as follows:

    # - C: Codificado
    # - D: Devengado

    # The structure of the new column names is: follow type ('Codificado', 'Devengado'),
    # month in number and the year. Eg: C-1-2021 means Codificado-Enero-2021.


    for t in range(len(months)):
        for j in range(len(colnames)):
            
            for i in range(len(flow_original)):
                if (months[t].lower() in colnames[j].lower()) and (flow_original[i].lower() in colnames[j].lower()):
                    
                    if len(str(t+1)) == 2:
                        colnames[j] = flow_type[i]+'-'+str(t+1)+'-'+str(year)
                        
                    else:
                        colnames[j] = flow_type[i]+'-'+'0'+str(t+1)+'-'+str(year)
                    
    PAI1 = df1.copy() # For Plan Anual de Inversiones
    PAI1.columns = colnames
    
    # this is for making it eassier to treat:
    
    for col in PAI1.columns[:4]:
    
        PAI1[col] = PAI1[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
        
        
    new_index = []

    # To set the new index of the data frame, it follows the next form: sector code+entity code+ project code* +
    # source code
    
    # * The project code was created with a counter. This is because it is repeated in different project of different
    # years in the raw data files.

    for i in PAI1.index:
        
        ind_entidad = PAI1['entidad'][i].split()
        PAI1['entidad'][i] = ' '.join(ind_entidad[2:])
        ind_entidad = ind_entidad[0]
        
        ind_sectorial = PAI1['sectorial'][i].split()
        PAI1['sectorial'][i] = ' '.join(ind_sectorial[2:])
        ind_sectorial = ind_sectorial[0]
        
        PAI1['proyecto'][i] = ' '.join(PAI1['proyecto'][i].split()[2:])
        
        # There are some cases when the name of one project is the same by other. We know that projects with the same name
        # are different thanks to the entity.
        
        if PAI1['proyecto'][i] not in index_dict:
            
            index_dict[PAI1['proyecto'][i]] = str(project_counter)
            project_counter+=1
        
        new_id = 'P'+index_dict[PAI1['proyecto'][i]]+'S'+ind_sectorial+'E'+ind_entidad
        
        new_index.append(new_id)
    
    PAI1['id'] = new_index
    
    return PAI1, index_dict, project_counter

pai_dict = {} # The own register of every project, conditional to it enitity and "sectorial"
PAI_counter=1 # Counter of previous projects

PAI, pai_dict, PAI_counter = cleanup(2017, pai_dict, PAI_counter)


# Apply cleanup function to all years
for y in [2018, 2019, 2020, 2021]:
    PAI1, pai_dict, PAI_counter = cleanup(y, pai_dict, PAI_counter)
    
    for i in PAI1.index:
            
        # This statement is to update the name of a project and avoid
        # repeat the id
        
        PAI['entidad'].loc[PAI['id'] == PAI1['id'][i]] = PAI1['entidad'][i]
        PAI['sectorial'].loc[PAI['id'] == PAI1['id'][i]] = PAI1['sectorial'][i]
    
    PAI = pd.concat([PAI, PAI1])

# I do not want the values "Pagados", "Inicial" and "fuente"
id_cols = ['id', 'proyecto', 'entidad', 'sectorial']
selected_cols = id_cols[:]


for year in ['2017', '2018', '2019', '2020', '2021']:
    PAI['C'+year] = PAI[[i for i in PAI.columns if year in i and 'C-' in i]].astype(float).sum(axis=1)
    PAI['D'+year] = PAI[[i for i in PAI.columns if year in i and 'D-' in i]].astype(float).sum(axis=1)
    
    selected_cols = selected_cols+['C'+year, 'D'+year]

PAI = PAI[selected_cols]
    
PAI = PAI.groupby( id_cols, as_index = False ).sum()

# Getting the total values of each type of flow.

PAI['ctotal'] = PAI[[i for i in PAI.columns if 'C' in i]].astype(float).sum(axis=1)
PAI['dtotal'] = PAI[[i for i in PAI.columns if 'D' in i]].astype(float).sum(axis=1)

PAI = PAI.set_index('id')

PAI.to_csv('pai.csv')