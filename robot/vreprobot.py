__author__ = 'li yan zhe'

from robot import robotdata
from leg import Leg
from vrep import vrep


class Vreprobot:
    width = robotdata.width
    length = robotdata.length
    height = robotdata.height
    orientation = [0, 0, 0]
    legs = []

    def __init__(self):
        """
        Initial method
        """
        vrep.simxFinish(-1)     # close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)

        self.legs = self.load_legs()
        self.i = 0
        vrep.simxSynchronous(self.clientID, True)

        print "connected with id ", self.clientID

    def finish_iteration(self):
        vrep .simxSynchronousTrigger(self.clientID)

    def get_joints(self):
        """
        Get the joints
        :return: joints of each leg
        """
        if self.clientID != -1:
            error_code, handles, int_data, float_data, array = vrep.simxGetObjectGroupData(
                self.clientID,
                vrep.sim_appobj_object_type,
                0,
                vrep.simx_opmode_oneshot_wait)

            data = dict(zip(array, handles))

            fl_leg = dict((key, value) for key, value in data.iteritems() if "fl" in key and "joint" in key)
            fr_leg = dict((key, value) for key, value in data.iteritems() if "fr" in key and "joint" in key)
            rr_leg = dict((key, value) for key, value in data.iteritems() if "rr" in key and "joint" in key)
            rl_leg = dict((key, value) for key, value in data.iteritems() if "rl" in key and "joint" in key)

            return fl_leg, fr_leg, rr_leg, rl_leg
        return None

    def load_legs(self):
        """
        Init legs
        :return: legs
        """
        width = self.width
        length = self.length
        height = self.height
        fl, fr, rr, rl = self.get_joints()
        rests = robotdata.legs_resting_positions
        legs = {
            "front_left": Leg("front_left", fl, self.clientID, (length / 2, width / 2, height), rests[0]),
            "front_right": Leg("front_right", fr, self.clientID, (length / 2, -width / 2, height), rests[1]),
            "rear_right": Leg("rear_right", rr, self.clientID, (-length / 2, -width / 2, height), rests[2]),
            "rear_left": Leg("rear_left", rl, self.clientID, (-length / 2, width / 2, height), rests[3]),
        }

        return legs
