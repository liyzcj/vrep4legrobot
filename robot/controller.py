__author__ = 'li yan zhe'

import time
from trotgait import Trotgait
from keylistener import Keylistener


class Controller:
    def __init__(self, robot):
        self.robot = robot
        self.dx = 10
        self.dy = 0
        self.dz = 0
        self.dro = [0, 0, 0]

        self.keyListener = Keylistener()
        self.startTime = time.time()
        self.trotgait = Trotgait(self.robot)

    def trot(self):
        """
        executes a step of the "trot" gait.
        """
        self.trotgait.iterate([self.dx, self.dy, self.dz], self.dro)

    def iterate(self):
        """
        runs one iteration of the code, usually called in a loop
        """
        try:
            self.read_keyboard()
        except Exception as e:
            print("could not read keyboard:", e)

        self.trot()
        self.robot.finish_iteration()
        time.sleep(0.005)

    def read_keyboard(self):
        """
        processed key inputs into dx ,dy, dz, dro values.
        :return:
        """
        if self.keyListener.get_key(119):
            dx = 1
        elif self.keyListener.get_key(115):
            dx = -1
        else:
            dx = 0
        if self.keyListener.get_key(97):
            dy = 1
        elif self.keyListener.get_key(100):
            dy = -1
        else:
            dy = 0
        if self.keyListener.get_key(114):
            dz = 1
        elif self.keyListener.get_key(102):
            dz = -1
        else:
            dz = 0
        if self.keyListener.get_key(116):
            self.dx = self.dy = self.dz = self.dro[2] = 0
        if self.keyListener.get_key(113):
            self.dro[2] -= 0.006
        elif self.keyListener.get_key(101):
            self.dro[2] += 0.006

        if self.keyListener.get_key(49):
            self.robot.disconnect()
        self.dx += dx
        self.dy += dy
        self.dz += dz
