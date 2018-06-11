# import time
import threading
import pythoncom
from robot import controller
from robot import vreprobot


robot = vreprobot.Vreprobot()
controller1 = controller.Controller(robot)
print("script ready!")


def run():
    global controller1
    while True:
        controller1.iterate()
