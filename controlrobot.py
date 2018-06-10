import time
from robot import controller
from robot import vreprobot


robot = vreprobot.Vreprobot()
controller1 = controller.Controller(robot)
print("script ready!")


def run():
    global controller1
    controller1.iterate()
