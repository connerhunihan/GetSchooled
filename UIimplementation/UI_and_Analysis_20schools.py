import tkinter as tk

import numpy as np
import pandas as pd
import random
import time
from sklearn.linear_model import LogisticRegression
"""
GetSchooled is the final project for Info206: Software Prototyping. It was created
by a group of graduate students at Berkeley's School of Information including:
	Alyssa Li
	Jake Mainwaring
	Michelle Peretz
	Conner Hunihan (www.connerhunihan.com)
The program is designed to help students find colleges.  
TO DO:
0. WHY ISN'T COLLEGE_SELECTION DEFINED?!?
1. Format – replacing pack() w/ grid()
"""

programmer_testing = False #during development print information to verify the code works - set to False to supress printing
	
LARGE_FONT = ("Verdana", 21)
SECOND_FONT = ("Verdana", 12)

states = []
match = []

list_of_answers = []
matched_schools = []

df = pd.read_csv('ConsolidatedSchools.csv')
df = df.iloc[:142]
choices_df = pd.read_csv('ProjectScenarios_revisedmp.csv')

def record_button_1(*args):
	record_selection(1)
def record_button_2(*args):
	record_selection(2)
def record_button_3(*args):
	record_selection(3)

def record_selection (scenario_choice):    
	list_of_answers.append(scenario_choice)
	if programmer_testing:
		print("list_of_answers: ", list_of_answers)

def erase_selections (*args):
	list_of_answers.clear()
	states.clear()
	match.clear()

class GetSchooled(tk.Tk):
	'''sets up the application, creates single page frame'''
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "GetSchooled")
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)	#0 sets minimum size, weight=1 is a priority thing
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		# generate pages from dictionary 
		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix, PageSeven, PageEight, PageNine, PageTen, PageEleven, PageTwelve, PageThirteen, PageFourteen, PageFifteen, PageSixteen, PageSeventeen, PageEighteen, PageNineteen, PageTwenty, ResultsPage, DisplayPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)

	def show_frame(self, cont):	
		'''raises frame to active view-level, cont dictrates which frame'''
		frame = self.frames[cont]
		frame.tkraise()		#raises frame to the front

	def get_match(self, StartPage):
		'''record matches coefficienct'''
		match.append(StartPage.matchEntered.get())
		if programmer_testing:
			print("Match level entered: ", match)
		return match

	def get_state(self, StartPage):
		'''record state(s) coefficient(s)'''
		states_input = StartPage.stateEntered.get()
		state_vals = [state.strip().upper() for state in states_input.split(",")]
		states.extend(state_vals)
		if programmer_testing:
			print("States entered: ", states)
		return states

class StartPage(tk.Frame):
	def __init__(self, parent, controller):	
		'''parent references the container parameter in F()...line61.  controller references the self in F()...line61'''
		tk.Frame.__init__(self, parent) #parent parameter references GetSchooled
		label = tk.Label(self, text="GetSchooled", font=LARGE_FONT)
		label.pack(pady=5, padx=5)

		# instantiate Label widget
		introText = tk.Label(self, text="THIS IS WHERE THE PROGRAM WILL GO", font=SECOND_FONT)
		# make Label widget appear with .pack()
		introText.pack(pady=10, padx=10)

		# create label and state entry widgets, make both appear w pack() function
		self.stateEntered = tk.StringVar()
		entryState_label = tk.Label(self, text="Please select which states you are interested in exploring (OR, WA, UT, etc.) \nPlease separate by commas, or enter \"all\" for all states: ").pack()
		entryState = tk.Entry(self, textvariable=self.stateEntered).pack()

		# create label and match entry widgets, make both appear w pack() function
		self.matchEntered = tk.StringVar()
		entryMatch_label = tk.Label(self, text="Please select matching level: \n0 to 4 (0=loose 4=strict): ").pack()
		entryMatch = tk.Entry(self, textvariable=self.matchEntered).pack()
		
		# create submit button that calls submit_entries function, when pressed
		submitButton = tk.Button(self, text="Click to submit", 
			command=lambda: self.submit_entries(PageOne, controller))
		submitButton.pack()

	def submit_entries (self, PageOne, app):
		'''app.GetEntries adds values to their respective lists; show_frame navigates to PageOne screen'''
		app.get_match(self)
		app.get_state(self)
		app.show_frame(PageOne)

class PageOne(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page One", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(0))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageTwo(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Two", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(1))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)


class PageThree(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Three", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(2))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
		

class PageFour(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Four", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(3))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageFive(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Five", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(4))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageSix))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageSix))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageSix))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)  

class PageSix(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Six", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(5))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageSeven))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageSeven))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageEight))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageSeven(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Seven", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(6))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageEight))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageEight))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageEight))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageEight(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Eight", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(7))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageNine))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageNine))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageNine))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageNine(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Nine", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(8))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageTen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageTen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageTen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
        
class PageTen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Ten", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(9))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageEleven))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageEleven))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageEleven))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageEleven(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Eleven", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(10))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageTwelve))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageTwelve))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageTwelve))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
        
class PageTwelve(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Twelve", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(11))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageThirteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageThirteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageThirteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageThirteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Thirteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(12))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFourteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFourteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFourteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
        
class PageFourteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Fourteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(13))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFifteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFifteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFifteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageFifteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Fifteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(14))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageSixteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageSixteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageSixteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageSixteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Sixteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(15))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageSeventeen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageSeventeen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageSeventeen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
        
class PageSeventeen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Seventeen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(16))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageEighteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageEighteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageEighteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageEighteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Eighteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(17))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageNineteen))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageNineteen))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageNineteen))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
        
class PageNineteen(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Nineteen", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(18))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageTwenty))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageTwenty))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageTwenty))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageTwenty(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Twenty", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		colleges = tk.StringVar()
		colleges.set(college_selection(19))
		display = tk.Label(self, textvariable=colleges)
		display.pack()

		# button click navigates to next page, button.bind handler records the button click value
		button1 = tk.Button(self, text="Select College 1", command=lambda: controller.show_frame(ResultsPage))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = tk.Button(self, text="Select College 2", command=lambda: controller.show_frame(ResultsPage))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = tk.Button(self, text="Select College 3", command=lambda: controller.show_frame(ResultsPage))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = tk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class ResultsPage(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Results", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		results = tk.StringVar()

		results.set(' ') ####

		# results.set('These are the results')

		display = tk.Label(self, textvariable=results)
		display.pack()

		calcButton = tk.Button(self, text="Calculate Results!", command=lambda: controller.show_frame(ResultsPage))
		calcButton.pack()
		calcButton.bind("<1>", lambda event, self=self: self.calculate_results())

		displayButton = tk.Button(self, text="SHOW ME", 
			command=lambda: controller.show_frame(DisplayPage))
		displayButton.pack(pady=25)

	def calculate_results(self):
		result = display_matched_schools()
		results = tk.StringVar()
		results.set(result)
		print("UI Method: ",results)
		display = tk.Label(self, textvariable=results, font=SECOND_FONT)
		display.pack()

		label = tk.Label(self, text="Do you want more information on these schools?", font=SECOND_FONT)
		label.pack(pady=10, padx=10)



class DisplayPage(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="School Information", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		calcButton = tk.Button(self, text="Show Detailed Information!", command=lambda: controller.show_frame(DisplayPage))
		calcButton.pack()
		calcButton.bind("<1>", lambda event, self=self: self.get_school_info())

		# pulls hypothetical colleges as a string returned from college_selection function
		results = tk.StringVar()

		results.set(' ') 
		# results.set('This is the display')
		display = tk.Label(self, textvariable=results)
		display.pack()

		startOverButton = tk.Button(self, text="START OVER", 
			command=lambda: controller.show_frame(StartPage))
		startOverButton.pack(pady=25)
		startOverButton.bind("<1>", erase_selections)
#==============================================================================
# 
#==============================================================================
	def get_school_info(self):
		result = display_school_info()
		results = tk.StringVar()
		results.set(result)
		print("UI Method: ",results)
		display = tk.Label(self, textvariable=results, font=SECOND_FONT)
		display.pack()


########################################################################################################################################################################################################

def college_selection(row_number):
	'''This function gathers all of the user input for fictional colleges. It cycles through 20 scenarios, with 3 colleges each, 
	and it adds each selection to list_of_answers. After converting them to 0's and 1's in a later step, these will be added 
	to the first column of the ProjectScenarios csv file".'''

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
	
	#this for loop goes through each of the actual schools in df, and adds a row to X_test dataframe for each sfchool
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

def calculate_matched_schools(list_of_answers):
	'''This function returns a list of matched schools based on the users preference.'''

	#Taking the list of answers and getting them into 0's and 1's
	state_choice = states
	print(states)
	matched_schools = []

	choice_column_unflattened = [[1, 0, 0] if item == 1 else [0, 1, 0] if item == 2 else [0, 0, 1] if item == 3 else 'None' for item in list_of_answers]
    
	#Flattening the nested list into a final list and then converting it to a one-dimensional array
	choice_column_not_array = [item for sub_list in choice_column_unflattened for item in sub_list]
	choice_column = np.array(choice_column_not_array)
	if programmer_testing:
		print(choice_column)
	print(choices_df.index.size, len(choice_column))
	choices_df['CHOICE'] = choice_column
	if programmer_testing:
		print("TESTING: ", choices_df)

	#using our 'score_schools function,'scored_schools' will contain the array of scores of all actual schools (df)
	match_level = 0 if len(match) == 0 else int(match[0])

	scored_schools = score_schools(choices_df, df, match_level)


	#we will now create a list called matched_schools which will contain tuples of the schools that match the user state choices and have a score of more than 0 (meaning they match). 
	#the list has tuples of each matching school (score of school, index in df)
	for i in range(len(df)):
		#user only schools that match user input for chosen states
		if len(state_choice) == 0:
			continue
		if (df['STABBR'][i] in state_choice or state_choice[0].upper() == "ALL") and scored_schools[i] > 0:
			matched_schools.append((scored_schools[i], i))
		#Negative score from decision_function = school is NOT a match
		# elif scored_schools[i] > 0:
			#save school score and school index into df (actual schools) in a list of tuples
			

	#Sort matched schools list by descending score (first item in list should be highest score)        
	
	print(len(matched_schools), matched_schools)
	matched_schools = sorted(matched_schools, reverse=True)
	return matched_schools


def display_matched_schools():
	'''This fucntion displays information about the top 10 matched schools or, if there are less than 10, the names of the schools that matched'''
	# Might want to comment back this line below in:
	print("I am being exectured now!")
	matched_schools = calculate_matched_schools(list_of_answers)
	schools = ""

	if len(matched_schools) > 0:
		n = 0 #counter for # of matches
		if len(matched_schools) > 9:
			#if there are at least 10 schools, we print the top 10
			response = 'Top 10 school matches from best to last fit: \n'
		else:
			#if there are less than 10 matches, we print this text
			response = 'School matches from best to last fit: \n'
		
		#loop for all matched schools
		for i in range(len(matched_schools)):
			#set df_index as the index into the df to extract data for the actual school that matched (index i)
			df_index = matched_schools[i][1]
			print(i, df_index)
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
					schools += "{}\t{}\n".format(n, df['INSTNM'][df_index])
				else:
					break

		print(response + schools)
		return response + schools
	else:            
		matches = 'Total Matches',len(matched_schools)
	return matches

def display_school_info():
    '''This function consolidates the specific information about the top 10 matched schools (name, ratio, percentile, size, town, admission rate, SAT score.)'''
	matched_schools = calculate_matched_schools(list_of_answers)
	n = 0
	school_info = ""
	for i in range(len(matched_schools)):       
		n += 1 #increase match school counter to present top 10
		if n < 11:
			df_index = matched_schools[i][1] #df_index is the index into df to get info on actual school[i]
			school_info += df['INSTNM'][df_index] + ":\n"
			school_info += '\tState of Institution: {}\n'.format(df['STABBR'][df_index])
			school_info += '\tStudent Faculty Ratio: {}\n'.format(df['SFRatio'][df_index])
			school_info += '\tSchool Ranking - Percentile: {}\n'.format(df['PERCENTILE'][df_index])
			school_info += '\tSchool Size: {}\n'.format(['Small','Mid-sized','Large'][int(df['ACTUAL SIZE (S/M/L)'][df_index])-1])
			school_info += '\tTown/City Size: {}\n'.format(['Large City','Mid-sized Town','Small Town'][int(df['URBANIZATION'][df_index])-1])
			school_info += '\tAdmission Rate: {}'.format(int(round(df['ADM_RATE'][df_index]*100))) + '\n'
			school_info += '-'*20 + '\n\n'
	
	return str(school_info)

app = GetSchooled()
app.mainloop()