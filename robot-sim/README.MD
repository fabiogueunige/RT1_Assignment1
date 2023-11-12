Python Robotics Assignment 1
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Assignment
----------------------

## Fast Explenation


* The code starts by initializing the robot and setting up constants and thresholds.
* It defines functions for motion, sensor readings, reaching tokens, operation management, and token transport.
* The main function initializes sets for seen and done tokens, performs an initial token discovery, and then transports the tokens to the station.
* It checks for additional tokens and transports them if found.
* Finally, the program terminates.





# Importing necessary libraries
from __future__ import print_function
import time
from sr.robot import *

# Initializing the robot
R = Robot()

# Setting up constants and thresholds
velocity = 10
tempo = 1/2
a_th = 2.0
d_th = 0.4
d_th_reach = 0.7 #to release 
disnear = 1.5
lap = 120

# Function to set linear velocity
function drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to set angular velocity
function turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to escape from the token
function turning_back(vel):
    drive(-6*vel, tempo)
    turn (5*velocity, 1.2)

# Function to find the closest token still not taken
function find_right_token(tkdone):
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
        return -1, -1, -1
    else:
        return dist, rot_y, tcode

# Function to find all the tokens
function find_all_token(tkseen, tkorigin):
    dist = 100
    for i in range(0, lap):
        for token in R.see():
            if token.info.code not in tkseen:
                dist = token.dist
                rot_y = token.rot_y
                tcode = token.info.code
                tkorigin.append([tcode, dist, rot_y])
                tkseen.add(tcode)
        if dist == -1:
            print("No token detected in the research of all")
        turn(4*velocity, tempo/20)

# Function to find the station
function get_station(tko):
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

# Function to reach the tokens
function reaching_token(dist, rot, tk, tkdone):
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
    elif rot < -a_th:
        turn(-velocity, tempo/4)
        drive(2*velocity, tempo/2)
        control = 2
    elif rot > a_th:
        turn(velocity, tempo/4)
        drive(2*velocity, tempo/2)
        control = 3
    else:
        turn(2*velocity, tempo)
    return control

# Function to manage the operations
function manager(distance, angle, tk, tkdone):
    control = -1
    while (control != 0):
        if tk not in tkdone:
            if (distance != -1):
                control = reaching_token(distance, angle, tk, tkdone)
            (distance, angle, tk) = find_right_token(tkdone)
            if (distance == -1):
                turn(velocity, tempo)
            elif (control != 0):
                control = reaching_token(distance, angle, tk, tkdone)
        else:
            (distance, angle) = get_station(tk)
            if (distance == -1):
                turn(velocity, tempo)
            else:
                control = reaching_token(distance, angle, tk, tkdone)

# Function to transport the tokens from their position to the station
function token_transport(tkseen, tkdone, tkorigin):
    distance = 0
    angle = 0
    while (len(tkseen) != len(tkdone)):
        (distance, angle, tc) = find_right_token(tkdone)
        manager(distance, angle, tc, tkdone)
        manager(distance, angle, tkorigin[0][0], tkdone)

# Main function
function main():
    tkseen = set()
    tkdone = set()
    counter = 0
    tkorigin = []
    drive(2*velocity, tempo)
    find_all_token(tkseen, tkorigin)
    tkdone.add(tkorigin[0][0])
    token_transport(tkseen, tkdone, tkorigin)
    print("Checking if there are other tokens")
    counter = len(tkseen)
    find_all_token(tkseen, tkorigin)
    if (counter - len(tkseen) != 0):
        token_transport(tkseen, tkdone, tkorigin)
    else:
        print("All the tokens have been found")
    print("The program terminates")
    exit()

# Execution
main()

