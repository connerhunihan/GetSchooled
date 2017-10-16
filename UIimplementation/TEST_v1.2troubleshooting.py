import tkinter as tk

import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression

programmer_testing = True

list_of_answers = [2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3]

df = pd.read_csv('ConsolidatedSchools.csv')
df = df.iloc[:142]
choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv')


match_level = ['0']
match_level = int(match_level[0])
state_choice = ['CA']

# def calculate_matched_schools():
#     choice_column_unflattened = [[1, 0, 0] if item == 1 else [0, 1, 0] if item == 2 else [0, 0, 1] if item == 3 else 'None' for item in list_of_answers]

#     choice_column_not_array = [item for sub_list in choice_column_unflattened for item in sub_list]
#     choice_column = np.array(choice_column_not_array)
    
#     choices_df['CHOICE'] = choice_column 

#     scored_schools = score_schools(choices_df,df,match_level)

#     for i in range(len(df)):

#         if df['STABBR'][i] not in state_choice and state_choice != 'ALL':
#             continue

#         if scored_schools[i] > 0:

#             matched_schools.append((scored_schools[i],i))

#     matched_schools = sorted(matched_schools,reverse=True)

def score_schools():
    ''' 
    This function scores all the actual schools (df) against the chosen scenarios.
    choices_df = dataframe for 60 school scenarios, 20 of them were chosen by the user (1 in CHOICE column) 
    df = dataframe for 142 actual schools that we will try to match with
    match_leve = the C level used in the log regression to determine strictness, as chosen by the user (user input: 0-4)
    '''
    match_level_list = [1000,1,0.1,0.01,0.05] # 0 = 1000, 1 = 1, 2 = 0.1, 3 = 0.01, 4 = 0.05. smaller the matching level (C parameter) the stricter the matching will be 
    
    X_train = choices_df.iloc[:, 1:9] #X_train is all rows in choices_df, columns 1-8 (exclude choice col which is col 0)
    Y_train = choices_df['CHOICE'] #Y_train is CHOICE col in choices_df, includes 1 for chosen scenario (20 of them), rest are 0. Needed to indicate selected scenarios to be included in logreg model 
    
    #create X_test which is an empty dataframe with columns corresponding to X_train (similar to column names in choices_df w/o CHOICE). It will later be populated with information from each actual school. 
    df_col = ['SFRATIO','SMALL','MID_SIZED','LARGE','PERCENTILE','SMALL_TOWN','MEDIUM_TOWN','LARGE_CITY']
    
    X_test = pd.DataFrame(columns=df_col)
 
    #use this array to populate values for town size and school size 
    size_values = [[1,0,0],[0,1,0],[0,0,1]]
    
    #this for loop goes through each of the actual schools in df, and adds a row to X_test dataframe for each school
    for i in range(len(df)):

        size_x = int(df['ACTUAL SIZE (S/M/L)'][i]) #val between 1 and 3, correspond to school size
        town_x = int(df['URBANIZATION'][i]) #val between 1 and 3, correspond to town size
        perc_value = float(df['PERCENTILE'][i].strip('%')) #convert % from text to numeric value, w/o % sign (in choices_df its a number, in df its a string)
        
        #Creat a list containing all information for one actual school, in the order of the choices_df columns
        one_school = [df['SFRatio'][i],
                      size_values[size_x-1][0],
                      size_values[size_x-1][1],
                      size_values[size_x-1][2],
                      round(perc_value),
                      size_values[town_x-1][2],
                      size_values[town_x-1][1],
                      size_values[town_x-1][0]]
        
        #convert one_school list into a dataframe with one row
        one_school_df = pd.Series(one_school, index=df_col)
        
        #append one_school dataframe row to X_test of the actual schools
        X_test = X_test.append(one_school_df,ignore_index = True)
        
        
    # Fitting the logistic regression model
    #scoring test schools against the training data 
    logreg = LogisticRegression(C=match_level_list[match_level])
    #the default c level is 1. if we don't want to ask users to select strictness leve, then remove what's inside the parentheses and remove the prompt at the start of the code. 

    #fit the model using the training data from scenario choices. X_train includes all 60 scenarios, only 20 will be fitted based on rows in Y_train that equal 1. 
    logreg.fit(X_train, Y_train)
     
    #run the decision_function method that will score the actual schools in X_test against the training data (20 scenarios). it will return an array (scores) with a score for each actual school. 
    scores = logreg.decision_function(X_test)


    if programmer_testing:
        #this only prints if programmer_testing = True. This prints information about each of the 20 scenario choice schools. We only print schools (X_train values) whose row in Y_train choice column = 1. 
        print('Schools Profile')
        for i in range(len(Y_train)):
            if Y_train[i] == 1:
                print('Ratio: ',X_train['SFRATIO'][i],end='\t')
                print('Percn: ',X_train['PERCENTILE'][i],end='\t')
                if X_train['SMALL'][i] == 1 :
                    colsize = 'Small'
                elif X_train['MID_SIZED'][i] == 1:
                    colsize = 'Med'
                else:
                    colsize = 'Large'
                    
                if X_train['SMALL_TOWN'][i] == 1 :
                    townsize = 'Small'
                elif X_train['MEDIUM_TOWN'][i] == 1:
                    townsize = 'Med'
                else:
                    townsize = 'Large'               
                print('College :',colsize,end='\t')
                print('Town: ',townsize)
    
    #our function returns the array of scores for each actual school

score_schools()