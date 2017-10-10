
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression
import analyze_weights as aw

file_name = '/Users/conner.hunihan/GitRepo/Info 206/final-project_GroupI'
df = pd.read_csv(file_name)

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


Urbanization_dict = {1: 'Large City', 2: 'Mid-sized town', 3: 'Small Town'}


# In[9]:

Urbanization_dict


# In[10]:

# Calculations
# Link for easy way to do calculations - https://www.youtube.com/watch?v=5TPNOC27bk0


# In[11]:

# Make sure to delete last two columns when doing logistic regression


# In[115]:

choices_df = pd.read_csv(file_name)


# In[116]:

choices_df.shape


# In[117]:

choices_df.head()


#USER INPUT STATE
#I programmed this so they enter in states "OR, WA, CA, etc." but we can change it to region. Just wanted to make sure it worked. We need a more comprehensive welcome message + ask for their name. 
state_choice = (input('Please select which states you are interested in exploring (OR, WA, UT, etc.) Please separate by commas): ')).upper()

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
logreg.fit(X, Y)

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

print(weights_df)

# In[136]:


# use function from analyze_weights (imported as a 'aw') to find corresponding values in df based on user preferences and return a list of possible schools
school_matches = aw.analyze_data(weights_df, df, state_choice)
if len(school_matches) == 0:
    print('no matches found!!!')
else:
    for i in school_matches:
        print(df['INSTNM'][i])
        
#need to find a way to represent the % importance of certain attributes 
        
    

