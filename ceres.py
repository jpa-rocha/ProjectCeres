import RPi.GPIO as GPIO
import argparse
import os
import sys
import devices as dev

# The ceres.py script is used to create the ceres CLI tool in order to have
# manual control of the system

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# parser set the initial options for the CLI including the name
parser = argparse.ArgumentParser(prog = 'ceres',
				description = 'Manual control for Project Ceres',
				add_help = True)

# when defining the arguments order is important, first the objects are
# defined and only after can the actions be defined.

# object defines which objects are available for the CLI
parser.add_argument('object',
                    choices=['pump', 'light', 'all'])

# action defines which actions are available for each object
parser.add_argument('action',
		 choices=['on', 'off', 'status'])

args = parser.parse_args()

# According to the 'object' called in the CLI the corresponding function is called
# with the given 'action'
if args.object == 'pump':
	dev.pump(args.action, 1)

if args.object == 'light':
	dev.light(args.action, 1)

if args.object == 'all':
	dev.pump(args.action, 1)
	dev.light(args.action, 1)
