from tkinter import *
from tkinter import ttk
import GetSchooled_UI

import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression


def setup():
    # set up the main window
    root = Tk()
    # title main window
    root.title("GetSchooled")

    # create frames – main and display 
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    choiceDisplay = ttk.Frame(mainframe, padding="3 3 12 12")
    # define dimensions of frame widget
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    choiceDisplay.grid(column=2, row=5, sticky=(N, W, E, S))

    # Create six widgets: 
    #   entry – state, match, college choice
    #   buttons – three college choices
    button1 = StringVar()
    button1.set("College 1")
    button2 = StringVar()
    button2.set("College 2")
    button3 = StringVar()
    button3.set("College 3")

    state = StringVar()
    match = StringVar()
    collegeChoice = StringVar()
    collegeChoice.set(college_selection())

    #PLACEHOLDER FOR COLLEGE CHOICE DISPLAY/DATA

    # initialize three entry widgets
    enterStateEntry = ttk.Entry(mainframe, width=30, textvariable=state)
    matchLevelEntry = ttk.Entry(mainframe, width=30, textvariable=match)
    # define dimensions
    enterStateEntry.grid(column=4, row=2, sticky=E)
    matchLevelEntry.grid(column=4, row=3, sticky=E)
    # initialize three college display buttons)
    ttk.Button(mainframe, text="College 1", textvariable=button1, command=recordCollege1).grid(column=2, row=6, sticky=W)
    ttk.Button(mainframe, text="College 2", textvariable=button2, command=recordCollege2).grid(column=3, row=6, sticky=W)
    ttk.Button(mainframe, text="College 3", textvariable=button3, command=recordCollege3).grid(column=4, row=6, sticky=E)

    # initialize labels
    ttk.Label(mainframe, text="This is introductory text that explains what the program does").grid(column=3, row=1, sticky=E)
    ttk.Label(mainframe, text='Please select which states you are interested in exploring (OR, WA, UT, etc.) \nPlease separate by commas, or enter "all" for all states: ').grid(column=2, row=2, sticky=(N, E))
    ttk.Label(mainframe, text='Please select matching level 0 to 4 (0=loose 4=strict): ').grid(column=2, row=3, sticky=(S, E))

    fictionalChoiceDisplay = Text(choiceDisplay, height=20, width=50)
    fictionalChoiceDisplay.insert('1.0', 'TEST')

    # finishing touches 
    #   adding padding to all widges that are children of mainframe
    #   initializes program with cursor focused on the first entry field
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    enterStateEntry.focus()

    # root.mainloop()

def college_selection (row_number):
    
    '''This function gathers all of the user input for fictional colleges. It cycles through 20 scenarios, with 3 colleges each, and it adds each selection to list_of_answers. After converting them to 0's and 1's in a later step, these will be added to the first column of the ProjectScenarios csv file".'''
    # if global counting variable < max, return None
        # test with a low number so that I don't have to run through so many loops
    row_number *= 3
    Size_dict = {1: 'Small (Less than 5,000 students)', 2: 'Mid-sized (5,000 - 15,000 students)', 3: 'Large (Greater than 15,000 students)'}
    Urbanization_dict = {1: 'Large City', 2: 'Mid-sized town', 3: 'Small Town'}

    college1 = ('COLLEGE 1' + '\n' + str(choices_df['SFRATIO'].iloc[row_number]) + ':1 Student-faculty ratio' + ' \n' + 
           Size_dict[choices_df['BODY_SIZE'].iloc[row_number]] 
           + '\n' + str(choices_df['PERCENTILE'].iloc[row_number]) 
           + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number]] + '\n')

    college2 = ('COLLEGE 2' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 1]) + ':1 Student-faculty ratio' + '\n' 
           + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 1]] 
           + '\n' + str(choices_df['PERCENTILE'].iloc[row_number+1]) 
           + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number+1]] + '\n')

    college3 = ('COLLEGE 3' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 2]) + ':1 Student-faculty ratio' + '\n' 
           + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 2]] 
           + '\n' + str(choices_df['PERCENTILE'].iloc[row_number + 2]) 
           + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number + 2]] + '\n\n')
        #can uncomment the line below and comment the input line to randomly select choices instead of manually entering 
        #scenario_choice = random.randint(1,3)  
        
    collegeArray = [college1, college2, college3]
    return collegeArray
        #can uncomment the line below and comment the input line to randomly select choices instead of manually entering 
        #scenario_choice = random.randint(1,3)  
    
    # list_of_answers.append(scenario_choice)
    # row_number += 3
    # print (list_of_answers)
    # return list_of_answers

def record_selection (scenario_choice):    
        list_of_answers.append(scenario_choice)
    # return list_of_answers

def score_schools(choices_df,df,match_level):
    ''' 
    This function scores all the actual schools (df) against the chosen scenarios.
    choices_df = dataframe for 60 school scenarios, 20 of them were chosen by the user (1 in CHOICE column) 
    df = dataframe for 142 actual schools that we will try to match with
    match_leve = the C level used in the log regression to determine strictness, as chosen by the user (user input: 0-4)
    '''
    match_level_list =[0.01, 0.05, 0.1, 1, 1000]
    # 4 = 1000, 3 = 1, 2 = 0.1, 1 = 0.01, 0 = 0.05. smaller the matching level (C parameter) the stricter the matching will be 
    
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
    return scores