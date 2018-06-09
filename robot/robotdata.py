__author__ = 'li yan zhe'

import numpy as np

width = 100
length = 150
height = 30

shoulderLength = 20
femurLength = 46
tibiaLength = 92

femurServoLimits = (-90, 65)
tibiaServoLimits = (-55, 90)
shoulderServoLimits = [-80, 80]

# rate to  transform pwm pulse to degrees
genericServoRate = -13.88

totalDistance = femurLength + tibiaLength


front = length/2
back = -length/2
left = width/2
right = -width/2
offset = totalDistance/2

resting_height = -50

cg_offset_x = 0

# front left, front right, back right, back left
legs_resting_positions = [(front + offset - cg_offset_x, left+offset, resting_height),
                          (front + offset - cg_offset_x, right-offset, resting_height),
                          (back - offset - cg_offset_x, right-offset, resting_height),
                          (back - offset - cg_offset_x, left+offset, resting_height)]

legs_resting_positions = np.array(legs_resting_positions)
