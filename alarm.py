#!/usr/bin/env python3.9

import sys
import time
import numpy
import pygame
import pygame.sndarray
from math import floor


def _ring(seconds: int, /):
	""" Rings the alarm for [seconds]
	
	[seconds] : int
	
	"""

	# Initializing pygame for playing audio
	pygame.mixer.pre_init(44100, -16, 1)
	pygame.init()

	# Load the notes we want to play
	low = _get_note(261.63)
	high = _get_note(392)

	# Play the one second alarm sound for the passed number of seconds.
	for i in range(seconds*10):
		_play_note(high, 50)
		_play_note(low, 50)


def _get_note(frequency: float, /):
	""" Calculates the note and returns a Sound object.

	[frequency] The frequency of the note e.g. 440 for A and 880 for A'
	"""

	# How many sound frames are there per wave
	frames = 44100/frequency

	# Put the sawtooth frames into an array.
	arr = numpy.array([16384 * (x % frames) / frames - 32768 for x in range(0, 44100)]).astype(numpy.int16)

	# Return a Sound object created from the wave frame array.
	return pygame.sndarray.make_sound(arr)


def _play_note(sound: pygame.mixer.Sound, duration: int, /):
	""" Plays the passed note for the passed duration.

	[note] The Sound object containing the note.
	[duration] The duration of the note in milliseconds.
	"""

	sound.play(-1)
	pygame.time.delay(duration)
	sound.stop()


def start_alarm_clock(alarm_hour: int, alarm_min: int, /):
	""" Starts an alarm that rings at the specified time.

	e.g.: startAlarmClock(14,9)
	[alarm_hour] the hour value of the time.
	[alarm_min] the minute value of the time.

	"""
	# Get the current time.
	now = time.localtime()
	
	# Put the hours and the minutes of the current time in variables.
	current_hour = now.tm_hour
	current_min = now.tm_min 
	
	# How many minutes do we have to wait?
	needed_min = alarm_min - current_min
	
	# If the value of minutes is smaller than the current times minutes.
	# e.g when it is 14:09 and you set the alarm for 15:06
	if needed_min < 0:
		# We need a positive value for the seconds.
		needed_min += 60
		# And we reduce the hours we need to wait by one.
		current_hour += 1
	
	# Now we check how much hours there are until the alarm rings.
	needed_hour = alarm_hour - current_hour
	
	# If the hour value is smaller than hour current time, we have a day switch in it.
	# e.g when it is 20:06 and you set the alarm for 19:06
	if needed_hour < 0:
		needed_hour += 24
		
	# If the user wants to set the current time as an alarm.
	if needed_hour == needed_min == 0:
		needed_hour = 24
	
	# Here we calc how many seconds we have to wait.
	wait_seconds = needed_min*60 + needed_hour*3600 - now.tm_sec
	
	# And now we calc our user output.
	needed_hour = floor(wait_seconds / 3600)
	needed_min = floor((wait_seconds - (needed_hour*3600))/60)
	needed_sec = floor(wait_seconds - needed_min*60 - needed_hour*3600)
	
	# Here we inform the user on how long he have to wait for his alarm.
	print("Alarm starts in {} hour(s), {} minute(s), and {} second(s)".format(needed_hour, needed_min, needed_sec))
	
	# Sleeping time!
	time.sleep(wait_seconds)
	
	# And time to wake up!!
	print("Wake up!!! <3")
	_ring(5)


def start_pomodoro(minutes: int, /):
	""" Starts pomodorolike alarm

	[minutes: int] In how many minutes the alarm should start.
	"""
	
	# Tell the user that the alarm will ring in the passed amount of minutes.
	print("Alarm rings in {} minute(s)".format(minutes))
	
	# Wait for the seconds.
	time.sleep(minutes*60)
	
	# Do the alarm call.
	print("Wake up!!!")
	_ring(5)


def _print_argument_error():
	""" Prints the help text
	"""
	print("Small alarm function for your console.")
	print("Usable with one or two numeric arguments")
	print()
	print("Sox must be installed with 'sudo apt-get install sox' to get an alarm sound.")
	print()
	print("One argument:")
	print("If there is only one argument it is interpreted as minutes. The alarm will act")
	print("as a pomodoro that rings after the set minutes.")
	print()
	print("Two arguments:")
	print("With two arguments, you will set a alarm clock for a specified time.")
	print("If you set 14 09 as arguments, the alarm will start at 14:09.")
	print("")
	print("On ubuntu you can put this task into background with 'ctrl+z' and then run 'bg'")
	print("Get it to the foreground again with fg")


# If the module is run as a script.
if __name__ == "__main__":

	# If the user entered two numeric parameter.
	if len(sys.argv) == 3 and sys.argv[1].isnumeric() and sys.argv[2].isnumeric():
	
		# The first parameter is the hour value of the set time.
		arg_hour = int(sys.argv[1])
		# The second parameter is the minute value of the set time.
		arg_minute = int(sys.argv[2])
		
		# Check if the hour and minute values are reasonable for a alarm clock time.
		if arg_hour >= 0 or arg_hour < 24 or arg_minute >= 0 or arg_minute < 60:
			# We start our alarm clock.
			start_alarm_clock(arg_hour, arg_minute)
		else:
			# Else we let the user know how to use this tool.
			_print_argument_error()
	
	# If the user entered one numeric parameter.
	elif len(sys.argv) == 2 and sys.argv[1].isnumeric():
	
		# Load the parameter as minutes.
		arg_minutes = (int(sys.argv[1]))
		
		# Check if the pomodoro is set to a reasonable time.
		if arg_minutes >= 0:
		
			# Start the pomodoro.
			start_pomodoro(arg_minutes)
	
		else:
			# Else we tell the user how he can use this tool.
			_print_argument_error()
			
	# Else there where the wrong number of arguments or they had the wrong type.
	else:
		# Show the help text.
		_print_argument_error()
