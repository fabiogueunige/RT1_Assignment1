from __future__ import print_function

import time
import signal
import os
from sr.robot import *

R = Robot()

"""
Possible procedure:
robot makes 360 to find all the tokens and puts them in list saving the distamces, the angle and the code of every one

From this list i take the medium distance and i try a way to find the right angle to go as near as possible to the center where 
i will put the first token and it will be used as arrival point for the other

run the code as:

    python3 run.py assignment.py 
"""

#########################
# VARIABLE DECLARATIONS #
#########################

velocity = 10 # velocity of the robot to move
tempo = 1/2 # time for the robot to move

""" float: Threshold for the control of the orientation"""
a_th = 2.0
""" float: Threshold for the control of the linear distance"""
d_th = 0.4 # treshold for the token to grab
d_th_reach = 0.7 # treshold for the token to release
disnear = 1.5 # distance to go slow

lap = 120 # number of laps to do

####################
# MOTION OPERATORS #
####################

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turning_back(vel):
    """
    Function to escape from the token

    Args: 
        vel (int): the speed of the wheels
    """
    drive(-6*vel, tempo)
    turn (5*velocity, 1.2) #90 degrees angle



###########
# SENSORS #
###########

def find_right_token(tkdone): 
    """
    Function to find the closest token

    Args:
        tkdone (set): set of all the token done

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
        tcode (int): code of the token (-1 if no token is detected)
    """
    dist = 100
    distmin = 100
    tcode = -1
    for token in R.see():
        if token.dist < distmin and token.info.code not in tkdone:
            dist = token.dist
            rot_y = token.rot_y
            tcode = token.info.code
            distmin = dist
            
    if dist == 100:
        return -1, -1,-1
    else:
        return dist, rot_y,tcode
    

def find_all_token(tkseen,tkorigin):
    """
    Function to find all the tokens 

    Args:
        tkseen (set): set of all the token seen
        tkorigin (list): list of all the token info

    Returns: 
        float: distance of the token
        float: angle between the robot and the token
    """
   

    dist = 100
  
    for i in range(0,lap): # 360 degrees rotation
        for token in R.see():
            if token.info.code not in tkseen:
                dist = token.dist
                rot_y = token.rot_y
                tcode = token.info.code
                tkorigin.append([tcode,dist,rot_y])
                tkseen.add(tcode)
                print("Info token: ", tcode, " ", dist, " ", rot_y)

        if dist == -1:
            print ("No token detected in the reserch of all")
        turn(4*velocity, tempo/20)


def get_station(tko):
    """
    Function to find the station
    
    Args:
        tko (int): code of the token
    Returns:
        dist (float): distance of the station (-1 if no station is detected)
        rot_y (float): angle between the robot and the station (-1 if no station is detected)
    """
    dist = 100
    distmin = 100   
    
    for token in R.see():
        if token.dist < distmin and token.info.code == tko:
            dist = token.dist
            rot_y = token.rot_y
            
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

            
###################
# MOTION TO TOKEN #
###################

def reaching_token(dist, rot, tk,tkdone):
    """
    Function to reach the tokens

    Args:
        dist (float): distance of the closest token
        rot (float): angle between the robot and the token
        tk (int): code of the token
        tkdone (set): set of all the token done
    
    Returns: 
        control (int): control variable for the manager
    """
    if dist < d_th and tk not in tkdone:
        R.grab()
        print("Taking the token ", tk)
        tkdone.add(tk)
        turning_back(velocity)
        control = 0 
    
    elif dist < d_th_reach and tk in tkdone:
        print("Leaving the token ")
        R.release()
        turning_back(velocity)
        control = 0

    elif -a_th <= rot <= a_th:  
            if dist < disnear:
                drive(5*velocity, tempo/4)
            else:
                drive(10*velocity, tempo/4)
            control = 1
    
    elif rot< -a_th:  
        turn(-2*velocity, tempo/12)
        drive(2*velocity,tempo/4)
        control =2
    
    elif rot> a_th:
        turn(+2*velocity, tempo/12)
        drive(2*velocity,tempo/4)
        control = 3
    
    else: 
        turn (12*velocity, tempo/12)
    
    return control


#####################
# OPERATION MANAGER #
#####################

def menager(distance,angle,tk,tkdone):
    """
    Function to manage the operations (taking or leaving the token)
    
    Args: 
        distance (float): distance of the closest token (-1 if no token is detected)
        angle (float): angle between the robot and the token (-1 if no token is detected)
        tk (int): code of the token

    """
    control = -1 # Control variable

    while (control !=0):
        if tk not in tkdone:
            if (distance != -1):
                control = reaching_token(distance, angle, tk,tkdone)
            
            (distance, angle, tk) = find_right_token(tkdone)
            if (distance == -1):
                turn(velocity,tempo)
            elif (control!=0):
                control = reaching_token(distance, angle, tk,tkdone)

        else:
            (distance, angle) = get_station(tk)
            if (distance == -1):
                turn(velocity,tempo)
            else:
                control = reaching_token(distance, angle, tk,tkdone)
                

    
###################
# TOKEN TRANSPORT #            
###################

def token_transport(tkseen,tkdone,tkorigin):
    """
    Function to bring the tokens from their position to the station

    Args: 
        tkseen (set): set of all the token seen
        tkdone (set): set of all the token done
        tkorigin (list): list of all the token info
    Input from other functions:
        distance (float): distance of the closest token (-1 if no token is detected)
        angle (float): angle between the robot and the token (-1 if no token is detected)
        tc (int): code of the token
    """

    distance = 0 # Distance from the token
    angle = 0 # Angle from the token

    while (len(tkseen) != len(tkdone)):
        # Find the closest token
        (distance, angle, tc) = find_right_token(tkdone)
        
        # Go to the token
        menager(distance,angle,tc,tkdone)
        
        # Go to the station
        menager(distance,angle,tkorigin[0][0],tkdone)
        #repeating all the sequence 
        


############
#   MAIN   #
############

def main():
    """ 
    Main function
    """
    tkseen = set() # All token seen
    tkdone = set() # All token done
    
    counter = 0
    # Tmp Token
    tkorigin = [] # All token info, can be useful
    start_time = time.time()  # Start time
    drive(2*velocity, tempo)

    # Start understanding the environment and his position with respect to the tokens
    find_all_token(tkseen,tkorigin)
    tkdone.add(tkorigin[0][0]) # Add the first token to the set of the token done

    # Go to the tokens seen
    token_transport(tkseen,tkdone,tkorigin)
    end_time = time.time()  # End time 
    elapsed_time1 = end_time - start_time # time for the first check

    while True:
        # Check if there are other tokens
        print("Checking if there are other tokens")
        counter = len(tkseen)
        find_all_token(tkseen,tkorigin)
        if (counter-len(tkseen)!=0):
            token_transport(tkseen,tkdone,tkorigin)
        else:
            print("All the tokens have been found")
            end_time = time.time()  # End time 
            elapsed_time2 = end_time - start_time # time for the first check
            break
    
    with open('time_log2.txt', 'a') as f:
        # f.write("New attempt\n")
        f.write(str(elapsed_time1) + '\n')
        f.write(str(elapsed_time2) + '\n')

    print("The program terminates")
    os.kill(os.getpid(), signal.SIGINT)
    exit()


###############
#  EXECUTION  #
###############

main()
