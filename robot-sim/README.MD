Python Robotics Assignment 1
================================

This is the explanetion of the `assignment.py` code through a pseudocode, seeing it step by step  

Assignment
----------------------

## Fast Explenation

* The code starts by initializing the robot and setting up constants and thresholds.
* It defines functions for motion, sensor readings, reaching tokens, operation management, and token transport.
* The main function initializes sets for seen and done tokens, performs an initial token discovery, and then transports the tokens to the station.
* It checks for additional tokens and transports them if found.
* Finally, the program terminates.

## Prerequisites:

You can find all the necessary information [here](https://github.com/fabiogueunige/RT1_Assignment1/blob/main/README.md)

## Running: 

```bash
  $ python3 run.py assignment.py 
```  

### Importing necessary libraries

### Initializing the robot  
Robot init

### Setting up constants and thresholds  
*velocity   : common velocity
*tempo      : common time
*a_th       : angle treshold
*d_th       : distance treshold to grab the token
*d_th_reach : distance treshold to release the token
*disnear    : distance to slow down Robot velocity
*lap        : number of turns to have always 360 degree 

### Library functions  

| Name     | Input                    | Return   | Description                       |
| ---------| ------------------------ | -------- | --------------------------------- |
| drive    | speed(int), seconds(int) | void     | Moves the Robot linear            |
| turn     | speed(int), seconds(int) | void     | Makes the robot turning on itself |


### Function to escape from the token  
Function to turn back on itself after taking a token or releasing it
    drive back 
    turn on himsself

### Function to find the closest token still not taken  
Function to find the nearest token to bring to the station (the release point)  
    dist to 100  
    distmin to 100 to compare distances  
    tcode to -1 for error checking  
    
    - for each token seen by the robot:  
        - if token distance is less than distmin and token is not in tkdone  
            dist to token.dist distance of the token  
            rot_y to token.rot_y angle of the token  
            tcode to token.info.code code of the token  
            distmin to dist to change the minimum distance   
    - if dist to 100 than no token seen  
        return all parameters as errors  
    - else:  
        return all the right parameters 

### Function to find all the tokens
Initial function to start a 360 degree of rotation to find all the token  of the arena 
    dist to 100 for error checking  
    - for all (and more to complete always the rotation) 360 rotation  
        - for each token seen by the robot:    
            - if token has never be seen by the robot before  
                dist to token.dist distance of the token  
                rot_y to token.rot_y angle of the token  
                tcode to token.info.code code of the token  
                tkorigin add al the information to a list (let so for next possible improvements)   
                tkseen add the token to the ones saw by the robot

        - if dist equal -1: error  
            print error message  

        turn to complete the rotation  


### Function to find the station  

function to arrive to the assembly point  

    dist to 100   
    distmin to 100 to compare distances  
    - for each token seen by the robot:   
        - if token distance is less than distmin and token is the first token seen by the robot   
            dist to token.dist distance of the token  
            rot_y to token.rot_y angle of the token
   
    - if dist to 100 than no token seen  
        return all parameters as errors  
    - else:  
        return all the right parameters

### Function to reach the tokens
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

### Function to manage the operations
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

### Function to transport the tokens from their position to the station
function token_transport(tkseen, tkdone, tkorigin):
    distance = 0
    angle = 0
    while (len(tkseen) != len(tkdone)):
        (distance, angle, tc) = find_right_token(tkdone)
        manager(distance, angle, tc, tkdone)
        manager(distance, angle, tkorigin[0][0], tkdone)

### Main function
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

### Execution  

main()

