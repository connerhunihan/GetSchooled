import tkinter as tk
from tkinter import ttk
from functions import *
"""
STILL NEED TO FIGURE OUT:
1. How to pass state & match choices from UI into the following:
state_choice = (input('Please select which states you are interested in exploring (OR, WA, UT, etc.) Please separate by commas, or enter "all" for all states: ')).upper()
match_level = int(input('Please select matching level 0 to 4 (0=loose 4=strict): ')) 

2. Can you explain how the GetSchooled class works?
3. Format – replacing pack() w/ grid()
4. Why is stateEntered not being read as defined?
"""
	
LARGE_FONT = ("Verdana", 21)
SECOND_FONT = ("Verdana", 12)
buttonChoices = []
list_of_answers = []
# row_number = 0

# Globally defined to be able to pass back/forth btwn UI and data layer
collegeList = []

def record_button_1(*args):
	record_selection(1)
def record_button_2(*args):
	record_selection(2)
def record_button_3(*args):
	record_selection(3)

# def submit_entries(*args):
# 	print(StartPage.entryState.get())
# 	print(StartPage.entryMatch.get())

def record_selection (scenario_choice):    
    list_of_answers.append(scenario_choice)
    print(list_of_answers)

def erase_selections (*args):
	list_of_answers.clear()

def return_state_and_match (*args):
	state = stateEntered.get()
	match = entryMatch.get()
	print(state, match)

class GetSchooled(tk.Tk):
	"""Sets up the UI for the program"""
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# tk.Tk.iconbitmap(self, default="GetSchooled_icon.ico")
		tk.Tk.wm_title(self, "GetSchooled")
		container = ttk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)	#0 sets minimum size, weight=1 is a priority thing
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):

			frame = F(container, self)
			
			self.frames[F] = frame
			
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)

	def show_frame(self, cont):	#cont dictates which key number frame to show on front
		frame = self.frames[cont]
		frame.tkraise()		#raises frame to the front

class StartPage(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)		#parent class is GetSchooled
		label = ttk.Label(self, text="GetSchooled", font=LARGE_FONT)
		label.pack(pady=5, padx=5)

		introText = ttk.Label(self, text="THIS IS WHERE THE PROGRAM WILL GO", font=SECOND_FONT)
		introText.pack(pady=10, padx=10)

		#ENTRY FRAME
		# entryFrame = ttk.Frame(self).grid(row=0, column=0)
		entryState_label = ttk.Label(self, text="Enter which states you are interested in").pack()
		stateEntered = tk.StringVar()
		entryState = ttk.Entry(self, textvariable=stateEntered).pack()

		entryMatch_label = ttk.Label(self, text="Enter how strict a match").pack()
		matchEntered = tk.StringVar()
		entryMatch = ttk.Entry(self, textvariable=matchEntered).pack()
	
		submitButton = ttk.Button(self, text="Click to submit", 
			command=lambda: controller.show_frame(PageOne))
		submitButton.pack()
		submitButton.bind("<1>", return_state_and_match)

	def return_state_and_match (self):
		state = stateEntered.get()
		match = entryMatch.get()
		print(state, match)


class PageOne(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Page One", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#PLACEHODLER FOR...STATE AND MATCH SUBMITTED ARE DEFAULT VALUES, STATE=DISABLED

		colleges = tk.StringVar()
		colleges.set(college_selection(0))
		display = ttk.Label(self, textvariable=colleges)
		display.pack()

		button1 = ttk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = ttk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = ttk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageTwo))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = ttk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageTwo(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Page Two", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#PLACEHODLER FOR...STATE AND MATCH SUBMITTED ARE DEFAULT VALUES, STATE=DISABLED

		colleges = tk.StringVar()
		colleges.set(college_selection(1))
		display = ttk.Label(self, textvariable=colleges)
		display.pack()

		button1 = ttk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = ttk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = ttk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageThree))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = ttk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)


class PageThree(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Page Three", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#PLACEHODLER FOR...STATE AND MATCH SUBMITTED ARE DEFAULT VALUES, STATE=DISABLED

		colleges = tk.StringVar()
		colleges.set(college_selection(2))
		display = ttk.Label(self, textvariable=colleges)
		display.pack()

		button1 = ttk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = ttk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = ttk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFour))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = ttk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)
		

class PageFour(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Page Four", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#PLACEHODLER FOR...STATE AND MATCH SUBMITTED ARE DEFAULT VALUES, STATE=DISABLED

		colleges = tk.StringVar()
		colleges.set(college_selection(3))
		display = ttk.Label(self, textvariable=colleges)
		display.pack()

		button1 = ttk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = ttk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = ttk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = ttk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)

class PageFive(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Page Five", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		#PLACEHODLER FOR...STATE AND MATCH SUBMITTED ARE DEFAULT VALUES, STATE=DISABLED

		colleges = tk.StringVar()
		colleges.set(college_selection(4))
		display = ttk.Label(self, textvariable=colleges)
		display.pack()

		button1 = ttk.Button(self, text="Select College 1", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_1)
		button1 = ttk.Button(self, text="Select College 2", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_2)
		button1 = ttk.Button(self, text="Select College 3", command=lambda: controller.show_frame(PageFive))
		button1.pack()
		button1.bind("<1>", record_button_3)

		resetButton = ttk.Button(self, text="RESET PROGRAM", 
			command=lambda: controller.show_frame(StartPage))
		resetButton.pack(pady=25)
		resetButton.bind("<1>", erase_selections)


app = GetSchooled()
app.mainloop()
