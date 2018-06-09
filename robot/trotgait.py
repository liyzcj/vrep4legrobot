__author__ = 'li yan zhe'

import math
import time
import robotdata
import numpy
from robot.transform import rotate_around_center, distance


class Trotgait:

    z_profile = [0, 0, 0, 0, 0, 10, 40, 40, 30, 7]  # leg height x time
    z_points = len(z_profile)
    startTime = 0
    stepDistance = 5000
    lastDelta = numpy.array([0, 0, 0])
    currentDistance = 0

    def __init__(self, robot):
        self.last_time = time.time()
        self.z_profile.append(self.z_profile[0])
        self.robot = robot
        self.legs = robot.legs
        self.group1 = [self.legs["front_left"], self.legs["rear_right"]]
        self.group2 = [self.legs["front_right"], self.legs["rear_left"]]

    def height_at_progression(self, pro):
        """
        returns the foot height at prog[0-1] of the foot movement overall
        """
        index = math.floor(pro * self.z_points)
        diff = pro * self.z_points - index
        value = self.z_profile[int(index)] + (self.z_profile[int(index + 1)] - self.z_profile[int(index)]) * diff

        pro = (pro if pro <= 0.5 else 1 - pro)
        speed = -0.5 + (pro * 2)

        return value, speed

    def iterate(self, linear_speed, angular_speed):
        """
        do all the calculation to move feet to next location
        """
        rests = robotdata.legs_resting_positions
        rotational_distance = distance(rests[0], rotate_around_center(rests[0], 'z', angular_speed[2]))
        this_distance = math.sqrt(
            linear_speed[0] ** 2 + linear_speed[1] ** 2 + linear_speed[2] ** 2) + rotational_distance
        self.currentDistance = (self.currentDistance + this_distance) % self.stepDistance

        # current feet height depends on distance (maybe should depend on time? )
        step_progression = self.currentDistance / self.stepDistance
        step_progression_alternate = (step_progression + 0.5) % 1.0

        height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)
        height_pair2, speed_direction_pair2 = self.height_at_progression(step_progression_alternate)

        for leg in self.group1:
            angular_offset = rotate_around_center(leg.resting_position, 'z', angular_speed[2]) - leg.resting_position
            total_offset = angular_offset - linear_speed
            offset = speed_direction_pair1 * total_offset
            offset[2] = height_pair1
            rotated_position = self.get_rotated_leg_resting_positions(leg, angular_speed)
            leg.move_to_pos(*(rotated_position + offset))

        for leg in self.group2:
            angular_offset = rotate_around_center(leg.resting_position, 'z', angular_speed[2]) - leg.resting_position
            total_offset = angular_offset - linear_speed
            offset = speed_direction_pair2 * total_offset
            offset[2] = height_pair2
            rotated_position = self.get_rotated_leg_resting_positions(leg, angular_speed)
            leg.move_to_pos(*(rotated_position + offset))

    @staticmethod
    def get_rotated_leg_resting_positions(leg, dro):
        roting = rotate_around_center(leg.resting_position, "x", dro[0])
        return rotate_around_center(roting, "y", dro[1])
