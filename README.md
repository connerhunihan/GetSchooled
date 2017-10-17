# Info206_GroupI - GetSchooled

Group members: Jake Mainwaring (jmainwaring@berkeley.edu,  GitHub username = jmainwaring), Alyssa Li (alyssa_li@berkeley.edu,  GitHub username = alyssali), Michelle Peretz (maperetz@berkeley.edu,  GitHub username = michelleap), Conner Hunihan (conner.hunihan@berkeley.edu,  GitHub username = connerhunihan)

The goal of our project was to help prospective students explore colleges. To approach this, we broke the process into a few steps – filtering out certain schools by location, determining which aspects of a college are most important to the user, and pairing these two data points to recommend certain colleges for further exploration.

You'll notice that the code is broken up into two components - the GUI and the program itself. The first ~780 lines are all related to the GUI, which was built using tkinter. The rest of the code runs the program's logic/number crunching - user selecting  schools from fictional scenarios, training the model, and recommending real schools. This portion utilizes a few libraries, including sklearn, numpy, and pandas.              

When testing the program, make sure you have downloaded the two CSV files. If they are downloaded and you still are having trouble accessing them, you may need to set a more specific path within the following quotation marks...df = pd.read_csv('ConsolidatedSchools.csv') and choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv'). Otherwise, the testing should be straightforward. Run the program, input states, select a looseness level, make your twenty selections from the fictional scenarios, click "Calculate Results!", and click "School Info" then "Show Detailed Information" for more info on your matches.       
