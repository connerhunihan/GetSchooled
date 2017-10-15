from UI import GetSchooled
import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression
# from UI import GetSchooled

programmer_testing = False #during development print information to verify the code works - set to False to supress printing

list_of_answers = []
matched_schools = []

df = pd.read_csv('ConsolidatedSchools.csv')
df = df.iloc[:142]
choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv')
choices_df.shape

class Schools():
    # def __init__(self, df, choices_df, list_of_answers):
    #     # actual schools csv and dataframe 'df'
    #     self.df = pd.read_csv('ConsolidatedSchools.csv')
    #     self.df = df.iloc[:142]
    #     # scenario schools csv and dataframe 'choices_df'
    #     self.choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv')
    #     self.choices_df.shape
    #     self.list_of_answers = list_of_answers

    def DisplayMatches(self):
        score_schools(choices_df, df, GetSchooled.get_match(StartPage))
        match_schools()
        print(display_match())

def college_selection (row_number, choices_df):
    '''This function gathers all of the user input for fictional colleges. It cycles through 20 scenarios, with 3 colleges each, 
    and it adds each selection to list_of_answers. After converting them to 0's and 1's in a later step, these will be added 
    to the first column of the ProjectScenarios csv file".'''
    choices_df.shape

    row_number *= 3
    Size_dict = {1: 'Small (Less than 5,000 students)', 2: 'Mid-sized (5,000 - 15,000 students)', 3: 'Large (Greater than 15,000 students)'}
    Urbanization_dict = {1: 'Large City', 2: 'Mid-sized town', 3: 'Small Town'}

    college1 = ('COLLEGE 1' + '\n' + str(choices_df['SFRATIO'].iloc[row_number]) + ':1 Student-faculty ratio' + ' \n' + Size_dict[choices_df['BODY_SIZE'].iloc[row_number]] + '\n' + str(choices_df['PERCENTILE'].iloc[row_number]) + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number]] + '\n')
    college2 = ('COLLEGE 2' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 1]) + ':1 Student-faculty ratio' + '\n' + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 1]] + '\n' + str(choices_df['PERCENTILE'].iloc[row_number+1]) + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number+1]] + '\n')
    college3 = ('COLLEGE 3' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 2]) + ':1 Student-faculty ratio' + '\n' + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 2]] + '\n' + str(choices_df['PERCENTILE'].iloc[row_number + 2]) + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number + 2]] + '\n')
    collegeList = college1 + "\n" + "\n" + college2 + "\n" + "\n" + college3
    return collegeList

def score_schools(choices_df,df,match_level):
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
    return scores

def calculate_matched_schools (list_of_answers):
    '''This function returns a list of matched schools based on the users preference.'''

    #Taking the list of answers and getting them into 0's and 1's
    choice_column_unflattened = [[1, 0, 0] if item == 1 else [0, 1, 0] if item == 2 else [0, 0, 1] if item == 3 else 'None' for item in list_of_answers]

    #Flattening the nested list into a final list and then converting it to a one-dimensional array
    choice_column_not_array = [item for sub_list in choice_column_unflattened for item in sub_list]
    choice_column = np.array(choice_column_not_array)
    choices_df['CHOICE'] = choice_column
    if programmer_testing:
        print("TESTING: ", choices_df)

    #using our 'score_schools function,'scored_schools' will contain the array of scores of all actual schools (df)
    scored_schools = score_schools(choices_df,df,match_level)

    #we will now create a list called matched_schools which will contain tuples of the schools that match the user state choices and have a score of more than 0 (meaning they match). 
    #the list has tuples of each matching school (score of school, index in df)
    for i in range(len(df)):
        #user only schools that match user input for chosen states
        if df['STABBR'][i] not in state_choice and state_choice != 'ALL':
            continue
        #Negative score from decision_function = school is NOT a match
        if scored_schools[i] > 0:
            #save school score and school index into df (actual schools) in a list of tuples
            matched_schools.append((scored_schools[i],i))

    #Sort matched schools list by descending score (first item in list should be highest score)        
    matched_schools = sorted(matched_schools,reverse=True)
    return matched_schools

def display_matched_schools (matched_schools):
    if len(matched_schools) > 0:
        n = 0 #counter for # of matches
        if not programmer_testing:
            #insert code to print user name, and other information (what states they chose (state_choice), level of strictness as applicable)
            if len(matched_schools) > 9:
                #if there are at least 10 schools, we print the top 10
                response = 'Top 10 school matches from best to last fit:'
            else:
                #if there are less than 10 matches, we print this text
                response = 'School matches from best to last fit:'
        
        #loop for all matched schools
        for i in range(len(matched_schools)):
            #set df_index as the index into the df to extract data for the actual school that matched (index i)
            df_index = matched_schools[i][1]
            if programmer_testing:
                #this is just for testing purposes 
                print(df['INSTNM'][df_index],matched_schools[i][0])
                print('Ratio: ',df['SFRatio'][df_index],end='\t')
                print('Percn: ',df['PERCENTILE'][df_index],end='\t')
                print('College :',['Small','Med','Large'][int(df['ACTUAL SIZE (S/M/L)'][df_index])-1],end='\t')
                print('Town: ',['Large','Med','Small'][int(df['URBANIZATION'][df_index])-1])
            else:
                #this prints the list of matched schools for users (only the top 10)
                n += 1
                if n < 11:
                    schools = n,'\t',df['INSTNM'][df_index]
        return response + schools      
    else:            
        matches = 'Total Matches',len(matched_schools)
        return matches

def display_school_info (matched_schools):
    n = 0
    for i in range(len(matched_schools)):       
        n += 1 #increase match school counter to present top 10
        if n < 11:
            df_index = matched_schools[i][1] #df_index is the index into df to get info on actual school[i]
            school_info = (str((df['INSTNM'][df_index])) +
            ('\tState of Institution        : ',df['STABBR'][df_index]) +
            ('\tStudent Faculty Ratio       : ',df['SFRatio'][df_index]) +
            ('\tSchool Ranking - Percnentile: ',df['PERCENTILE'][df_index]) +
            ('\tSchool Size                 : ',['Small','Mid-sized','Large'][int(df['ACTUAL SIZE (S/M/L)'][df_index])-1]) +
            ('\tTown/City Size              : ',['Large City','Mid-sized Town','Small Town'][int(df['URBANIZATION'][df_index])-1]) +
            ('\tAdmission Rate              : ', str(int(round(df['ADM_RATE'][df_index]*100))) + '%'))
    return school_info

