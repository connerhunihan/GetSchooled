from functions import *

def main():
	setup()

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

if __name__ == '__main__':
	main()