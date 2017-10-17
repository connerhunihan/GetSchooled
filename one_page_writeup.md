The goal of our project was to help prospective students explore colleges. To approach this, we broke the process into a 
few steps – filtering out certain schools by location, determining which aspects of a college are most important to the user, 
and pairing these two data points to recommend certain colleges. The first step of filtering by location is simple – users 
input which states they are considering, and schools from any other state are removed. To calculate importance, we presented 
twenty scenarios of three fictional schools and had users select one for each scenario, where schools were described in 
terms of size, urbanization, ranking, and student: faculty ratio. These are entirely fictional and can be found in the 
“fictional_project_scenarios.csv”, which we pulled into our program using pandas. We made sure the attributes were generally 
distributed across scenarios (i.e. the three schools from one scenario are large/medium/small, have high/medium/low rankings) 
so that user preferences became clearer. The schools’ attributes serve as the feature variables, while the user’s choices 
serve as the response variable, and a logistic regression model is trained on this data. We took the coefficients for each 
variable – ranking, student: faculty ratio, etc. – rescaled them, and used them as rough proxies for which attributes most 
heavily influence the user’s colleges choice. From there, we paired this information with data on actual colleges, which is 
in the “consolidated_schools.csv” file, also using pandas to pull this in. For example, if a user said she wants to stay in 
California, the model that’s calculated from her sample school choices is used to score actual California schools. The 
colleges that best fit her model are then suggested to her.

In terms of challenges, the primary one was consolidating a list of real universities to pull from. This is described in 
more detail in the “Data Aggregation.txt” file, but the biggest difficulty was that no one data source had all of the 
schools and attributes we wanted to include. This required us to combine multiple sources of data (both automatically 
and manually). Another challenge was deciding which features to include. To do so, we talked to friends and family who are
currently applying to colleges and asked which attributes they care most about. Based on these conversations and the data 
we had available, we decided on ranking, student: faculty ratio, urbanization, and size. We also had issues adding a scrollbar 
through the tkinter library, and opted to only show four schools (which fits on the page) instead of ten. Given more time, 
we would have been able to better format the string output from the GUI.    

As a quick note, it’s important to download the csv files from our GitHub before testing out the program. You 
will also have to import libraries like pandas and scikit-learn. Generally, the best way to test this program is 
to use it as if you were a fictional user with certain criteria in mind. For example, trying it as if you wanted 
to stay in Massachusetts and care about student faculty ratio, or as if you were not bound to any state but only 
value ranking (which might return Stanford, Princeton, etc.) You can also test it out with less extreme scenarios and see 
which schools are recommended. From the testing we’ve done, the recommendations have been fairly relevant. Please let us 
know if you have any questions while looking through the project! 
