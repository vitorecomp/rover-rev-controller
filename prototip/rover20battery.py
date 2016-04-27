import pygame
from rover import Revolution
import time
import pygame
import sys
import signal
import subprocess
import tempfile
import os

tank = Revolution()

# Define some colors
BLACK	= (   0,   0,   0)
WHITE	= ( 255, 255, 255)

# Threshold for faster speed
SPEED_THRESH       = 0.5

# This is a simple class that will help us printL to the screen
# It has nothing to do with the joysticks, just outputing the
# information.


pygame.init()


pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

def axis_to_dir(axis):
	return round(axis)
	d = 0

	if axis > 0:
		d = 1
	elif axis < 0:
		d = -1

	return d


# -------- Main Program Loop -----------
while done==False:
	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop

		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released.")



	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	print("Number of joysticks: {}".format(joystick_count) )

	# For each joystick:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()

		print("Joystick {}".format(i) )


		# Get the name from the OS for the controller/joystick
		name = joystick.get_name()
		print("Joystick name: {}".format(name) )

		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = joystick.get_numaxes()
		print("Number of axes: {}".format(axes) )


		for i in range( axes ):
			axis = joystick.get_axis( i )
			print("Axis {} value: {:>6.3f}".format(i, axis) )
			if i == 2:
				tank.moveCameraHorizontal(round(axis))
			if i == 3:
				tank.moveCameraVertical(round(axis))

		axis2 = -joystick.get_axis(1)
		axis3 = -joystick.get_axis(0)
		goslow = False if abs(axis3) > SPEED_THRESH or abs(axis2) > SPEED_THRESH else True
		wheeldir = -axis_to_dir(axis3)
		steerdir = 0
		if(joystick.get_axis(5) > 0):
			steerdir = 1
		if(joystick.get_axis(4) > 0):
			steerdir = -1

		tank.drive(steerdir, wheeldir, goslow)

		buttons = joystick.get_numbuttons()
		print("Number of buttons: {}".format(buttons) )


		for i in range( buttons ):
			button = joystick.get_button( i )
			print("Button {:>2} value: {}".format(i,button) )
			if i == 10:
				if button == 1:
					pygame.quit ()
					tank.close()
					sys.exit()


		# Hat switch. All or nothing for direction, not like joysticks.
		# Value comes back in an array.
		hats = joystick.get_numhats()
		print("Number of hats: {}".format(hats) )


		for i in range( hats ):
			hat = joystick.get_hat( i )
			print("Hat {} value: {}".format(i, str(hat)) )





	# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

	# Go ahead and update the screen with what we've drawn.

	# Limit to 20 frames per second
	clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
tank.close()
