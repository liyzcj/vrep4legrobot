# vrep4legrobot
Use python to implement to control 4 legs simulated robot on V-REP！

## Requirement

- **Windows operation**
- V-REP 3.2.0 (32 bits) | go to [here](http://www.coppeliarobotics.com/previousversions.html) download  
- python 2.7  (32 bits)
- numpy
- pywin32 (32 bits)     | download from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32)
- pyHook (32 bits)      | download from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)


## Notes

- a bug in pyHook  
One function will be error in pyHook, which the **argument is "msg", replace it with "int(str(msg))"**

## install

- Download V-REP 3.2.0 (32 bit) and unzip in windows.
- Open vrep.exe
- load scene(4legs_scene.ttt) in V-REP
- User python 2.7 interpreter
- run **controlrobot.py**

## Operation

Key      |        Action
---------|---------------
W        |      Go Ahead
S        |      Go Back
A        |      Go Left
D        |      Go Right
Q        |      Turn Left
E        |      Turn Right
R        |    Higher Frequent
F        |    Lower Frequent
