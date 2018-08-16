import subprocess
import random
from pynput.keyboard import Key, Controller
import sys, time
import pandas as pd

#keyboard simulate
keyb = Controller()
actions = [Key.up,Key.down,Key.left,Key.right]
action_dict = {'U':Key.up,'D':Key.down,'L':Key.left,'R':Key.right}
score = 0
new_score = 0

state = (0,0,0)

#QTable

QTable = pd.DataFrame(collumns='state','U','D','R','L')


#Hyperparameters
epsilon = 1.0
min_epsilon - 0.05
epsilon_dim = 0.001
'''
add hyperparameters
- learning rate
- epsilon (exploration/exploitation)
- epsilon diminish rate
- no. of episodes
'''


'''
add ml loop
'''


proc =  subprocess.Popen(['python','C:\ML_Python\Car_simula\\rectangle_point_QTable_1.py'],shell=True, stdout=subprocess.PIPE)
print(proc)



while proc.poll() is None:
    line = proc.stdout.readline()
    line = line.decode('utf-8').split()

    #look for state in Qtable
    Qstate = QTable[QTable.state==state]

    #indicator if any action value for given state is empty
    #Qstate_action_null = Qstate.isnull().values.any()

    rnd = random.random()


    if Qstate.empty or rnd < epsilon:
        #exploration
        choosen_act = random.choice(actions)


    else:
        #exploitation
        Qaction = Qstate.iloc[:,1:5].astype(float).idxmax(axis=1)
        Qaction_value = Qaction.values[0]
        choosen_act =  action_dict.get(Qaction_value)

    # read output from car
    if line != []:
        if line[0] == 'cardata':
                speed = line[1]
                angle = line[2]
                dist  = line[3]
                new_score = int(line[4])

    score_diff = new_score - score
    score = new_score


    '''
    choose Qtable or random
    '''

    print(score_diff)


    keyb.press(choosen_act)
    keyb.release(choosen_act)


'''
update/add reward for state and choosen action
'''


'''
append state if not exists
'''

'''
add points loss on crash
'''

'''
v2.0
- introduce series of states
'''
