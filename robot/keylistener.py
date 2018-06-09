import pyHook
import pythoncom


class Keylistener:

    """
    This class hooks into keyboard events, and saves the states of each key into a dictionary.
    """
    keyMap = {}

    def pressed(self, event):
        self.keyMap[event.Ascii] = True
        # Debug
        # print self.keyMap[event.Ascii]

    def released(self, event):
        self.keyMap[event.Ascii] = False
        # Debug
        # print self.keyMap[event.Ascii]

    def get_key(self, key):
        if key in self.keyMap:
            return self.keyMap[key]
        else:
            return False

    def __init__(self):
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.pressed
        self.hm.KeyUp = self.released
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()

    def __del__(self):
        self.hm.UnhookKeyboard()


# Debug
if __name__ == "__main__":
    Keylistener()
