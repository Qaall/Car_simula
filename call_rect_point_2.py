import subprocess
import random
from pynput.keyboard import Key, Controller
import sys, time
import pandas as pd

#keyboard simulate
keyb = Controller()
actions = ['U','D','L','R']
action_dict = {'U':Key.up,'D':Key.down,'L':Key.left,'R':Key.right}


old_action_symbol = None
score = 0
new_score = 0

#initiate state parameters
speed = 0
angle = 0
dist = 0
state = (0,0,0)
state = str(state)

#QTable

QTable = pd.DataFrame(columns=['state','U','D','R','L'])
#set state as index
QTable = QTable.set_index('state')

#Hyperparameters
epsilon = 1.0
min_epsilon = 0.05
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


proc =  subprocess.Popen(['python','D:\Projects_MachineL\Car_simula\\rectangle_point_QTable_1.py'],shell=True, stdout=subprocess.PIPE)
print(proc)



while proc.poll() is None:
    line = proc.stdout.readline()
    line = line.decode('utf-8').split()
    if line != []:
        if line[0] == 'cardata':
            print("\n---------------'\nreceived line start: ",line)
            #look if state is present in Qtable
            print("state &&: ",state)
            Qstate = QTable.index.isin([state]).any()
            print("czy znaleziono:  -- ",Qstate)

            #indicator if any action value for given state is empty
            #Qstate_action_null = Qstate.isnull().values.any()

            rnd = random.random()


            if not Qstate or rnd < epsilon:
                #exploration
                action_symbol = random.choice(actions)
                choosen_act = action_dict.get(action_symbol)

            else:
                #exploitation
                Qaction = Qstate.iloc[:,1:5].astype(float).idxmax(axis=1)
                action_symbol = Qaction.values[0]
                choosen_act =  action_dict.get(action_symbol)

            # read output from car
            speed = line[1]
            angle = line[2]
            dist  = line[3]
            new_score = int(line[4])



            print("score:",score)
            score_diff = new_score - score
            score = new_score
            new_state = (int(speed), int(angle), dist)

            current_Qstate = pd.Series({old_action_symbol:score_diff},name=state)

            print("wybrana akcja + wynik:",current_Qstate,"\n||||||||")
            # ADD new / APPEND existing row to QTable
            if old_action_symbol != None:
                if Qstate:
                    QTable.set_value(state,old_action_symbol,score_diff)
                else:
                    QTable = QTable.append(current_Qstate)

            #assign new state to state
            state = str(new_state)
            old_action_symbol = action_symbol
            print("received line before keypress: ",line)

            print("key choosen to press: ",choosen_act)
            keyb.press(choosen_act)
            keyb.release(choosen_act)

print(QTable)

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
