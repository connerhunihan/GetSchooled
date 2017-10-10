
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression
df = pd.read_csv('ConsolidatedSchools.csv')


# In[4]:

# Good here
df = df.iloc[:142]


# In[5]:

df.tail(8)


# In[13]:

# As of now, I'm thinking of not having this in the latter section...Eight one-hots is a pain
# df['REGION'].unique()


# In[14]:

# Dictionaries


# In[6]:

Size_dict = {1: 'Small (Less than 5,000 students)', 2: 'Mid-sized (5,000 - 15,000 students)', 3: 'Large (Greater than 15,000 students)'}


# In[7]:

Size_dict[1]


# In[8]:

#I think these are switched? 
Urbanization_dict = {1: 'Large City', 2: 'Mid-sized town', 3: 'Small Town'}


# In[9]:

Urbanization_dict


# In[10]:

# Calculations
# Link for easy way to do calculations - https://www.youtube.com/watch?v=5TPNOC27bk0


# In[11]:

# Make sure to delete last two columns when doing logistic regression


# In[115]:

choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv')


# In[116]:

choices_df.shape


# In[117]:

choices_df.head()


#USER INPUT STATE 
state_choice = (input('Please select which states you are interested in explorin (separated by commas): ')).upper()

input("Now it's time to make your choices! Press enter to continue.")
# In[118]:

list_of_answers = []

def college_selection ():
    
    row_number = 0
    
    while row_number < 60:
        print ('COLLEGE 1' + '\n' + str(choices_df['SFRATIO'].iloc[row_number]) + ':1 Student-faculty ratio' + ' \n' + 
               Size_dict[choices_df['BODY_SIZE'].iloc[row_number]] 
               + '\n' + str(choices_df['PERCENTILE'].iloc[row_number]) 
               + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number]] + '\n')

        print ('COLLEGE 2' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 1]) + ':1 Student-faculty ratio' + '\n' 
               + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 1]] 
               + '\n' + str(choices_df['PERCENTILE'].iloc[row_number+1]) 
               + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number+1]] + '\n')

        print ('COLLEGE 3' + '\n' + str(choices_df['SFRATIO'].iloc[row_number + 2]) + ':1 Student-faculty ratio' + '\n' 
               + Size_dict[choices_df['BODY_SIZE'].iloc[row_number + 2]] 
               + '\n' + str(choices_df['PERCENTILE'].iloc[row_number + 2]) 
               + '% more presigious than other schools\n' + Urbanization_dict[choices_df['CITY_SIZE'].iloc[row_number + 2]] + '\n\n')

        scenario_choice = int(input("Please select one of the colleges: "))
        list_of_answers.append(scenario_choice)
        row_number += 3


# In[119]:

college_selection()


# In[120]:

list_of_answers


# In[68]:

# Taking the list of answers and getting them into 0's and 1's


# In[121]:

choice_column_unflattened = [[1, 0, 0] if item == 1 else [0, 1, 0] if item == 2 else [0, 0, 1] if item == 3 else 'None' 
            for item in list_of_answers]

choice_column_unflattened


# In[122]:

# Flattening the nested list into a final list and then converting it to a one-dimensional array
choice_column_not_array = [item for sub_list in choice_column_unflattened for item in sub_list]
choice_column = np.array(choice_column_not_array)
choice_column


# In[71]:

# Add it to the first column of choices_df


# In[123]:

# Don't need to actually run this each time 
choices_df.head()


# In[124]:

choices_df['CHOICE'] = choice_column


# In[125]:

choices_df.head()


# In[126]:

# Splitting into features (X) and response variable (Y)


# In[127]:

X = choices_df.iloc[:, 1:9]
X.head()


# In[128]:

Y = choices_df['CHOICE']


# In[129]:

# Fitting the logistic regression model
logreg = LogisticRegression()
modelfit = logreg.fit(X, Y)

#FAKE school values below:
X_test = choices_df.iloc[0:1, 1:9].copy()
Y_test = Y.iloc[:1].copy()
Y_test[0] = 1
X_test['SFRATIO'] = 15
X_test['SMALL'] = 0
X_test['MID_SIZED'] = 1
X_test['LARGE'] = 0


X_test['PERCENTILE'] = 96


X_test['SMALL_TOWN'] = 0
X_test['MEDIUM_TOWN'] = 0
X_test['LARGE_CITY'] = 1

#score fake school against model 
score_val = modelfit.score(X_test, Y_test)

print('score:',score_val)

input('if it shows 1 it means the "actual school" (the numbers i made up above) match the training data from the scenarios. if its 0, it doesnt. If we extend this to work with the enter consolidated schools csv then we can match our actual schools to the model')


training_accuracy=logreg.score(X,Y)
print ('Training Accuracy:',training_accuracy*100)


# In[130]:

weights_array = logreg.coef_
weights_array


# In[131]:

# Need to transform SFRatio and Percentile to make more sense with the odds ratio


# In[132]:

# Weights when I choose small student body each time - positive coefficient of 2.5
# array([[-0.10031511,  2.51294231 (small), -0.92401006 (medium), -1.3571143 (large) , -0.00315815,
#         -0.46032258,  0.14316328,  0.54897726]])

# Weights when I choose large student body each time - positive coefficient of 2.5 
# # array([[ -4.03373112e-02,  -1.53126501e+00,  -1.23935733e+00,
#           2.46841559e+00,   7.36315076e-04,   3.79584782e-01,
#          -4.64804309e-01,  -2.16987215e-01]])

# 1.6 for small town when I always select that one and 1.7 for large city when I always select that. Slightly lower
# than 2.5 because there is more perfect separation in school size (always small/medium/large) vs. in city,
# there are more where one scenario has two large cities


# In[133]:

# Because of this ^^, I had to multiply the SFRATIO and PERCENTILE values to reflect importance accurately


# In[134]:

weighted_df_cols = ['SFRATIO', 'SMALL', 'MID_SIZED', 'LARGE', 'PERCENTILE', 'SMALL_TOWN', 'MEDIUM_TOWN', 'LARGE_CITY']


# In[135]:

weights_df = pd.DataFrame(weights_array, columns = weighted_df_cols)
weights_df['SFRATIO'] = weights_df['SFRATIO']*4.5
weights_df['PERCENTILE'] = weights_df['PERCENTILE']*30


# In[136]:

print(weights_df)

def analyze_data(weights_df, df, state_choice):
    #STUDENT/FACULTY RATIO
    ratio_min = -1.010103
    ratio_max = 1.480083
    ratio_data_min = min(df['SFRatio'])
    ratio_data_max = max(df['SFRatio'])

    #assuming we figured out correct min and max ratio values, we find the value in the school dataset that corresponds to the weight value found from their choices. 
    #https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    #https://math.stackexchange.com/questions/377169/calculating-a-value-inside-one-range-to-a-value-of-another-range
    sfratio_value_array = ratio_data_min + (weights_df['SFRATIO']-ratio_min) * (ratio_data_max-ratio_data_min)/(ratio_max - ratio_min)
     
    sfratio_value = sfratio_value_array[0]
    
    sfratio_margin = (ratio_data_max - ratio_data_min)/10
    
    print(sfratio_value)
    
    #PRESTIGE/PERCENTILE
    percentile_max = 2.280571
    percentile_min = -1.882555
    percentile_data_min = float(min(df['PERCENTILE']).strip('%'))
    percentile_data_max = float(max(df['PERCENTILE']).strip('%'))
    
    
    percentile_value = percentile_data_min + (weights_df['PERCENTILE'][0]-percentile_min) * (percentile_data_max -percentile_data_min)/(percentile_max - percentile_min)
    
    percentile_margin = (percentile_data_max - percentile_data_min)
    
    #SCHOOL SIZE
    small_school = weights_df['SMALL'][0]
    mid_school = weights_df['MID_SIZED'][0]
    large_school = weights_df['LARGE'][0]
    
    if small_school > mid_school:
        school_size_value = 1
        if large_school > small_school:
            school_size_value = 3
    else:
        school_size_value = 2
        if large_school > mid_school:
            school_size_value = 3
        
    #TOWN SIZE/URBANIZATION -- problem?? 
    small_town = weights_df['SMALL_TOWN'][0]
    medium_town = weights_df['MEDIUM_TOWN'][0]
    large_city = weights_df['LARGE_CITY'][0]
    
    if small_town > medium_town:
        town_size_value = 1
        if large_city > small_town:
            town_size_value = 3
    else:
        town_size_value = 2
        if large_city > medium_town:
            town_size_value = 3
    
    
    school_matches_index = []
    for i in range(len(df)):
        if df['STABBR'][i] not in state_choice:
            continue
        if int(df['ACTUAL SIZE (S/M/L)'][i]) == school_size_value and int(df['URBANIZATION'][i]) == town_size_value:
            if sfratio_value >= df['SFRatio'][i] - sfratio_margin and sfratio_value <= df['SFRatio'][i] + sfratio_margin:
                percentile_float = float(df['PERCENTILE'][i].strip('%'))
                if percentile_value >= percentile_float - percentile_margin and percentile_value <= percentile_float + percentile_margin:
                    school_matches_index.append(i)
    #creates a list with the index into the df for that particular school
    return school_matches_index 

school_matches = analyze_data(weights_df, df, state_choice)
if len(school_matches) == 0:
    print('no matches found!!!')
else:
    for i in school_matches:
        print(df['INSTNM'][i])
        
    


# mp - create a new dataframe that tells us which ones columns have a abs.value that is larger than 0.5. 

#values_df = pd.DataFrame(abs(weights_array) > 0.5, columns = weighted_df_cols)

    
    

