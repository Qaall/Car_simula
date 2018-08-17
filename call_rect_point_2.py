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
rotate = 0
dist = 0
angle = 0
state = (0,0,0,0)
state = str(state)

#QTable

QTable = pd.DataFrame(columns=['state','U','D','R','L'])
#set state as index
QTable = QTable.set_index('state')

#Hyperparameters
epsilon = 1.0
min_epsilon = 0.05
epsilon_dim = 0.01
episod_no = 0
episodes = 200
'''
add hyperparameters
- learning rate
'''

#score file
fscore = open('score.txt','w')
fqtable = open('qTable.txt','w')

'''
add ml loop
'''


proc =  subprocess.Popen(['python','C:\ML_Python\Car_simula\\rectangle_point_QTable_1.py'],shell=True, stdout=subprocess.PIPE)
print(proc)


while proc.poll() is None and episod_no <= episodes:
    line = proc.stdout.readline()
    line = line.decode('utf-8').split()
    if line != []:
        if line[0] == 'cardata':

            #look if state is present in Qtable

            Qstate = QTable.index.isin([state]).any()


            #indicator if any action value for given state is empty
            #Qstate_action_null = Qstate.isnull().values.any()

            rnd = random.random()


            if not Qstate or rnd < epsilon:
                #exploration
                action_symbol = random.choice(actions)
                choosen_act = action_dict.get(action_symbol)

            else:
                #exploitation
                Qrow = QTable.loc[state]
                Qaction = Qrow.idxmax(axis=1)
                action_symbol = Qaction
                choosen_act =  action_dict.get(action_symbol)

            # read output from car
            speed = line[1]
            rotate = line[2]
            dist  = line[3]
            angle = line[4]
            new_score = int(line[5])



            score_diff = new_score - score
            score = new_score
            new_state = (int(speed), int(rotate), dist, angle)

            current_Qstate = pd.Series({old_action_symbol:score_diff},name=state)

            # ADD new / APPEND existing row to QTable
            if old_action_symbol != None:
                if Qstate:
                    QTable.set_value(state,old_action_symbol,score_diff)
                else:
                    QTable = QTable.append(current_Qstate)

            #assign new state to state
            state = str(new_state)
            old_action_symbol = action_symbol

            keyb.press(choosen_act)
            keyb.release(choosen_act)
        elif line[0] == 'endtime':
            episod_no += 1

            if epsilon > min_epsilon:
                epsilon  -= epsilon_dim
            print("---> ---> SCORE: ",score)
            print("-----epsilon: ",epsilon)

            fscore.write(str(score) + '\n')

fscore.close()
fqtable.write(str(QTable))
fqtable.close()

print('x end')


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
