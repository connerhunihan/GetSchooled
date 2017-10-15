import tkinter as tk
from functions import *
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
1. Format – replacing pack() w/ grid()
"""

programmer_testing = True #during development print information to verify the code works - set to False to supress printing
	
LARGE_FONT = ("Verdana", 21)
SECOND_FONT = ("Verdana", 12)

states = []
match = []

def record_button_1(*args):
	record_selection(1)
def record_button_2(*args):
	record_selection(2)
def record_button_3(*args):
	record_selection(3)

def record_selection (scenario_choice):    
    list_of_answers.append(scenario_choice)
    if programmer_testing == True:
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
		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, ResultsPage, DisplayPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)

	def show_frame(self, cont):	#cont dictates which key number frame to show on front
		'''raises frame to active view-level'''
		frame = self.frames[cont]
		frame.tkraise()		#raises frame to the front

	def GetMatch(self, StartPage):
		'''record matches coefficienct'''
		match.append(StartPage.matchEntered.get())
		if programmer_testing == True:
			print("Match level entered: ", match)
		return match

	def GetState(self, StartPage):
		'''record state(s) coefficient(s)'''
		states.append(StartPage.stateEntered.get())
		if programmer_testing == True:
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
		app.GetMatch(self)
		app.GetState(self)
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
		colleges.set(college_selection(0))
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
		colleges.set(college_selection(0))
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
		colleges.set(college_selection(0))
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
		colleges.set(college_selection(0))
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
		results.set(Schools.DisplayMatches(self))
		display = tk.Label(self, textvariable=results)
		display.pack()

		label = tk.Label(self, text="Do you want more information on these schools?", font=SECOND_FONT)
		label.pack(pady=10, padx=10)

		displayButton = tk.Button(self, text="SHOW ME", 
			command=lambda: controller.show_frame(DisplayPage))
		displayButton.pack(pady=25)

class DisplayPage(tk.Frame):
	'''this class instantiates as a whole-window frame'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="School Information", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		# pulls hypothetical colleges as a string returned from college_selection function
		results = tk.StringVar()
		# results.set('''Class.Schools.DisplayInfo''')
		display = tk.Label(self, textvariable=results)
		display.pack()

		startOverButton = tk.Button(self, text="START OVER", 
			command=lambda: controller.show_frame(StartPage))
		startOverButton.pack(pady=25)
		startOverButton.bind("<1>", erase_selections)

app = GetSchooled()
app.mainloop()
