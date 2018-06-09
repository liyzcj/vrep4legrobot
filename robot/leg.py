__author__ = 'li yan zhe'

import numpy as np
from math import *
import robotdata
from vrep import vrep


class Leg:

    """
    Leg implementation for V-REP simulation robot, it's responsible for moving and locating each leg.
    """
    footPosition = [0, 0, 0]
    angles = [0, 0, 0]

    def __init__(self, name, handles, client_id, position, resting_positions):
        """
        Initial a leg
        :param name: leg name, used to get its pointing direction in some implementations
        :param handles: handles information
        :param client_id: client id
        :param position: robot position
        :param resting_positions: feet resting position
        """
        self.name = name
        self.handles = handles
        self.clientID = client_id
        self.position = position
        self.resting_position = resting_positions
        self.shoulderLength = robotdata.shoulderLength
        self.tibiaLength = robotdata.tibiaLength
        self.femurLength = robotdata.femurLength
        self.torque = 1

        for key in self.handles:
            if "shoulder" in key:
                self.shoulderHandle = self.handles[key]
            elif "femur" in key:
                self.femurHandle = self.handles[key]
            elif "tibia" in key:
                self.tibiaHandle = self.handles[key]
        print(self.name, self.handles)

        self.yDirection = -1 if "right" in self.name else 1

    def ik_to(self, x0, y0, z0):
        """
        Inverse kinematics
        Calculates each joint angle to get the leg to coordinates x0,y0,z0
        :return: the correct angles
        """
        # math adapted from http://arduin0.blogspot.fi/2012/01/inverse-kinematics-ik-implementation.html
        dx = x0 - self.position[0]
        dy = y0 - self.position[1]
        dz = z0 - self.position[2]

        sl = self.shoulderLength
        fl = self.femurLength
        tl = self.tibiaLength

        x, y, z = dy * self.yDirection, -dz, -dx * self.yDirection

        tibia_angle = acos(((sqrt(
                ((sqrt(
                    x ** 2 + z ** 2)) - sl) ** 2 + y ** 2)) ** 2 - tl ** 2 - fl ** 2) / (-2 * fl * tl)) * 180 / pi
        shoulder_angle = atan2(z, x) * 180 / pi
        femur_angle = (((atan(((sqrt(x ** 2 + z ** 2)) - sl) / y)) + (acos((tl ** 2 - fl ** 2 - (
                sqrt(((sqrt(x ** 2 + z ** 2)) - sl) ** 2 + y ** 2)) ** 2) / (-2 * fl * (
                    sqrt(((sqrt(x ** 2 + z ** 2)) - sl) ** 2 + y ** 2)))))) * 180 / pi) - 90

        return radians(shoulder_angle), radians(femur_angle), radians(tibia_angle - 90)

    def move_to_pos(self, x, y, z):
        """
        Move the foot to coordinates [x,y,z]
        """
        try:
            angles = self.ik_to(x, y, z)
            self.move_to_angle(*angles)

            self.footPosition = np.array([x, y, z])
            self.angles = angles

        except Exception as exc:
            print (exc)

    def move_by(self, pos):
        """
        attempts to move it's foot my an offset of it's current position
        """
        target = self.position + pos
        self.move_to_pos(*target)

    def check_limits(self, shoulder_angle, femur_angle, tibia_angle):
        """
        Checks if the desired angles are inside the physically possible constraints.
        """
        shoulder_angle = degrees(shoulder_angle)
        femur_angle = degrees(femur_angle)
        tibia_angle = degrees(tibia_angle)

        femur_servo_limits = robotdata.femurServoLimits
        shoulder_servo_limits = robotdata.shoulderServoLimits
        tibia_servo_limits = robotdata.tibiaServoLimits

        if self.yDirection == -1:
            shoulder_servo_limits = [-shoulder_servo_limits[1], -shoulder_servo_limits[0]]

        if femur_angle < femur_servo_limits[0]:
            raise Exception("femur out of bounds")
        if femur_angle > femur_servo_limits[1]:
            raise Exception("femur out of bounds")
        if tibia_angle < tibia_servo_limits[0]:
            raise Exception("tibia out of bounds")
        if tibia_angle > tibia_servo_limits[1]:
            raise Exception("tibia out of bounds")
        if shoulder_angle < shoulder_servo_limits[0]:
            raise Exception(self.name, ":shoulder out of bounds, attempted {0}".format(shoulder_angle))
        if shoulder_angle > shoulder_servo_limits[1]:
            raise Exception(self.name, ":shoulder out of bounds, attempted {0}".format(shoulder_angle))

    def move_to_angle(self, shoulder_angle, femur_angle, tibia_angle):
        """
        Moves V-REP legs with proper orientations to desired angles.
        """
        vrep.simxSetJointTargetPosition(self.clientID,
                                        self.shoulderHandle,
                                        shoulder_angle,
                                        vrep.simx_opmode_oneshot)

        vrep.simxSetJointTargetPosition(self.clientID,
                                        self.femurHandle,
                                        femur_angle * self.yDirection,
                                        vrep.simx_opmode_oneshot)

        vrep.simxSetJointTargetPosition(self.clientID,
                                        self.tibiaHandle,
                                        tibia_angle * self.yDirection,
                                        vrep.simx_opmode_oneshot)
