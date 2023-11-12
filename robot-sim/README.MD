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

function to move the robot to the prefixed point:  

    - if dist less than dist treshold and token not taken yet  

        robot grab the token

        print he has taken it  

        tkdone.add(tk) add token to the released ones

        turning_back(velocity) to rotate on it self 

        control to 0 value return that means he finished the task

    - else if dist less than treshold to release the token and token in list of released one

        print he is leaving the token

        robot release the token

        turning_back(velocity)  rotate on itself

        control to 0  


    - else if angle is less than the treshold

        - if dist less than treshold for proximity :  

            drive slow

        - else:  

            drive fast

        control to 1 to say he is straight

    - else if  rot less than negative angle treshold:  

        turn left

        drive really slow

        control to 2  to say he is turning left

    - else if  rot bigger than positive angle treshold:  

        turn right  

        drive really slow

        control to 3  to say he is turning right

    else:  

        turn to check again 

    return control to give info about his state   


### Function to manage the operations
function that plan the operations of the Robot 
 
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

function that calls the menager operation for the complete process of every token one by one  

    distance = 0  

    angle = 0  

    while (len(tkseen) != len(tkdone)):  

        (distance, angle, tc) = find_right_token(tkdone)  

        manager(distance, angle, tc, tkdone)  

        manager(distance, angle, tkorigin[0][0], tkdone)  


### Main function

main function to make the programm runnable
    tkseen create a set to save all the token seen  

    tkdone create a set to save all the token left to the station  

    counter = 0 init of a length counter  

    tkorigin create a matrix with all the information of the token (when they are seen for the first time)  

    drive to move the Robot at the beginning  

    find_all_token(tkseen, tkorigin)  

    tkdone.add(tkorigin[0][0]) add the first token seen as the station  

    token_transport(tkseen, tkdone, tkorigin) to start the process for all tokens

    print is checking for all tokens  

    counter = as dimension of tkseen vector to save the tmp

    find_all_token(tkseen, tkorigin) check if he completes for all  

    if (counter - len(tkseen) is different from 0):  

        token_transport(tkseen, tkdone, tkorigin) restart the function for the ones forgiven  

    else:  

        print he has found all the tokens  

    print that he has finished his task


### Execution  

main()

