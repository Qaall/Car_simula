import pygame
from pygame.math import Vector2
import math
import random
from pynput.keyboard import Key, Controller
import numpy as np
import sys


pygame.init()

#keyboard simulate
keyb = Controller()

displ_width = 800
displ_height = 600


car_size = 10

displ = pygame.display.set_mode((displ_width,displ_height))

white = (255,255,255)
black = (0,0,0)
blue = (24,150,224)
green = (0,124,0)
blue2 = (73,107,163)


#objects
rect_1 = pygame.Rect(displ_width/2.3,100,200,10)


pygame.display.set_caption('test_title')


#main variables


clock = pygame.time.Clock()


font = pygame.font.Font(None, 30)


#### generating Qtable

QTable = np.zeros((1,1))





## intersect functions
def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def is_intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def line(p1, p2):
	A = (p1[1] - p2[1])
	B = (p2[0] - p1[0])
	C = (p1[0]*p2[1] - p2[0]*p1[1])
	return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    x = Dx / D
    y = Dy / D
    return x,y
###############################################################

## distance funct #############################################

def dist(p1,p2):
	distance = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
	return distance

###############################################################


## sigmoid function ########################################

def sig(x):
	return (x-60)/(4+abs(x-60))
############################################################

## angle function #########################################

def angl(p1,p2):
	x1,y1 = p1[0], p1[1]
	x2,y2 = p2[0], p2[1]

	deltax = x2 - x1
	deltay = y2 - y1
	angle_rad = math.atan2(deltay,deltax)
	angle_deg = angle_rad*180.0/math.pi
	return angle_deg

## score function ########################################

def score(speed, wall_dist):
	if wall_dist > 0:
		dist_sigmoid = sig(wall_dist)
	else:
		dist_sigmoid = 1
	score = abs(speed)*dist_sigmoid
	return score
###########################################################


#walls
lw_start, lw_end = (0,0),(0,displ_height)
tw_start, tw_end = (0,0),(displ_width,0)
rw_start, rw_end = (displ_width,0),(displ_width,displ_height)
dw_start, dw_end = (0,displ_height),(displ_width,displ_height)
left_wall = line(lw_start,lw_end)
top_wall = line(tw_start,tw_end)
right_wall = line(rw_start,rw_end)
down_wall = line(dw_start,dw_end)

# Main Loop

def gameLoop():

# changable variables
	gExit = False

	xpoint = displ_width/4
	ypoint = displ_height/2


	vector_one = Vector2(0,1)
	speed = 0
	angle = 0
	rangle = 0
	game_score = 0
	wall  = 0



# timer #############################################
	start_ticks=pygame.time.get_ticks() #starter tick
######################################################

#main game loop
	while not gExit:
		actions = [Key.up,Key.down,Key.left,Key.right]
		choosen_act = random.choice(actions)
		#keyb.press(choosen_act)
		#keyb.release(choosen_act)
		for event in pygame.event.get():
			#QUIT
			if event.type == pygame.QUIT:
				gExit = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					speed += 1
					speed = min(speed,10)
				if event.key == pygame.K_DOWN:
					speed -= 1
					speed = max(speed,-10)
				if event.key == pygame.K_LEFT:
					angle -= 1
					angle = max(angle,-4)
				if event.key == pygame.K_RIGHT:
					angle += 1
					angle = min(angle,4)


		vector_one.rotate_ip(angle)
		vectorx_smooth = round(vector_one[0],1)
		vectory_smooth = round(vector_one[1],1)
		xpoint += vectorx_smooth*-speed
		ypoint += vectory_smooth*-speed
		#print(vector_one,"--",vectorx_smooth,vectory_smooth,speed,"--",angle)
		car = pygame.Rect(xpoint,ypoint,car_size,car_size)

## timer #############################################
		seconds=round(((pygame.time.get_ticks()-start_ticks)/1000),0) #calculate how many seconds
######################################################
	# crossover
		# if xpoint > displ_width/2.3 and xpoint < displ_width/2.3 + 200 or xpoint+car_size > displ_width/2.3 and xpoint+car_size < displ_width/2.3 + 200:
		#     print ("x collision")


		if car.colliderect(rect_1) or xpoint < 0 or xpoint > displ_width or ypoint <0 or ypoint > displ_height:
			game_score -= 99
			speed = 0
			angle = 0
			xpoint = displ_width/4
			ypoint = displ_height/2

		if seconds>30.0:
			print("endtime")
			gameLoop()

			# canvas draw
		displ.fill(white)

		pygame.draw.rect(displ,black,rect_1)
		pygame.draw.rect(displ,blue,car)


		#speed vector direction
		if speed == 0:
			speedv = -1
		else:
			speedv = speed/abs(speed)

		#testline

		line_start=(xpoint,ypoint)
		line_end=(xpoint+200*-vectorx_smooth*(speedv),ypoint+200*-vectory_smooth*(speedv))

		rect_1_start=(rect_1.left,rect_1.bottom)
		rect_1_end=(rect_1.right,rect_1.bottom)

		line_car = line(line_start,line_end)
		line_rect = line(rect_1_start,rect_1_end)

		pygame.draw.line(displ,green,line_start,line_end)

## timer ##############################
		displ.blit(font.render(str(seconds), True, (black)), (displ_width-48, 24))


		#if tru then standad intersection
		# + angle between lines
		if is_intersect(line_start,line_end,rect_1_start,rect_1_end):
			intersect_p=(intersection(line_car,line_rect))
			wall = dist(line_start,intersect_p)
			rangle = angl(line_start,intersect_p)
		elif is_intersect(line_start,line_end,lw_start,lw_end): #left wall
			intersect_p=(intersection(line_car,left_wall))
			wall = dist(line_start,intersect_p)
			rangle = angl(line_start,intersect_p)
		elif is_intersect(line_start,line_end,tw_start,tw_end): #top wall
			intersect_p=(intersection(line_car,top_wall))
			wall = dist(line_start,intersect_p)
			rangle = angl(line_start,intersect_p)
		elif is_intersect(line_start,line_end,rw_start,rw_end): #right wall
			intersect_p=(intersection(line_car,right_wall))
			wall = dist(line_start,intersect_p)
			rangle = angl(line_start,intersect_p)
		elif is_intersect(line_start,line_end,dw_start,dw_end): #down wall
			intersect_p=(intersection(line_car,down_wall))
			wall = dist(line_start,intersect_p)
			rangle = angl(line_start,intersect_p)
		else:
			wall = 0
			rangle = 0
		## elif intersect with 2nd object
		## elif intersect with 3rd object
		## ....
		## elif intersect with nth object
######################################################

## score  ################################
		rangle = round(rangle,-1)
		wall = round(wall, -1)
		game_score += score(speed,wall)
		game_score = int(game_score)

		print('cardata', speed, angle, wall, rangle, game_score)
		sys.stdout.flush()
		displ.blit(font.render(str(game_score), True, (blue)), (24, 24))
		#displ speed and rotate
		displ.blit(font.render('spd:'+str(speed), True, (blue2)), (12, 48))
		displ.blit(font.render('rot:'+str(angle), True, (blue2)), (12, 72))
		#displ angle
		displ.blit(font.render('rot:'+str(rangle), True, (blue2)), (12, 96))
		'''
		intersection with multiple objects
		'''

		'''
		saving score at end
		'''

		pygame.display.update()
		clock.tick(10)

	pygame.quit()
	quit()

gameLoop()
