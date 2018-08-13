import subprocess
import random
from pynput.keyboard import Key, Controller
import sys, time

#keyboard simulate
keyb = Controller()
actions = [Key.up,Key.down,Key.left,Key.right]



#subprocess.call(['python','D:\Projects_MachineL\Python_rectangle\\rectangle_point_QTable_1.py'],stdout=subprocess.PIPE)

proc =  subprocess.Popen(['python','D:\Projects_MachineL\Python_rectangle\\rectangle_point_QTable_1.py'],shell=True, stdout=subprocess.PIPE)
print(proc)
print('x')

while proc.poll() is None:
    line = proc.stdout.readline()

    print(line)
    choosen_act = random.choice(actions)
    print(choosen_act)
    keyb.press(choosen_act)
    keyb.release(choosen_act)






'''
add scor diff retrival
'''

'''
add state (speed, angle, wall dist) retrival
'''

'''
append state if not exists
