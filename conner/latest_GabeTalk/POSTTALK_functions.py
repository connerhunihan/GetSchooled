from tkinter import *
from tkinter import ttk


# *args means function can be called by passing whatever argument (including none)
# FILL OUT FUNCTIONS WITH LOGIC TO RECORD A "1" FOR THE BUTTON CLICKED, TO PASS INTO THE INITIAL+EXPLORE PROGRAM
def recordCollege1(*args):
	Initial+Exploration_decisionfunctionMP,CH.record_selection(1)

def recordCollege2(*args):
	Initial+Exploration_decisionfunctionMP,CH.record_selection(2)

def recordCollege3(*args):
	Initial+Exploration_decisionfunctionMP,CH.record_selection(3)

def getState(*args):
	try: 
		value = str(state.get())
		state.set(value)
		return state
	except ValueError:
		pass

def getMatch(*args):
	try: 
		value = int(match.get())
		match.set(value)
		return match
	except ValueError:
		pass
    
# set up the main window
root = Tk()

# title main window
root.title("GetSchooled")

# create frames – main and display 
mainframe = tkk.Frame(root, padding="3 3 12 12")
choiceDisplay = ttk.Frame(mainframe, padding="3 3 12 12")
# define dimensions of frame widget
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
choiceDisplay.grid(column=2, row=5, sticky=(N, W, E, S))

# Create six widgets: 
#	entry – state, match, college choice
#	buttons – three college choices
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
#	adding padding to all widges that are children of mainframe
#	initializes program with cursor focused on the first entry field
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
enterStateEntry.focus()

root.mainloop()

# class ApplicationGUI:
# 	"""Sets up the UI for the program"""

# 	def __init__(self, master):
# 		self.master = master
# 		master.title('GetSchooled')
		
# 		self.introText = Text(master, text="This is introductory text that explains what the program does")
# 		self.introText.grid(column=0, row=0)
		
# 		self.statesEntry = Entry(master)
# 		self.statesEntry.grid(column=0, row=1, columnspan=3)
# 		self.matchEntry

# 		self.progressBar
# 		self.display

# 		self.button1
# 		self.button2
# 		self.button3

# def update():
# 	a

# def college_selection():
# 	a

# def record_selection():
# 	a

# def score_schools():
# 	a