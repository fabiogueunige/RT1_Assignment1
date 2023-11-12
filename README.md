Python Robotics Simulator
================================

Short Descpription
--------------------------------

This is the first assignment for the Reserch Track I course of Robotics Engineering Master Degree in Genoa.  
CHANGE
This project consists into move a robot to take all the tokens in the space and to put all of them toghether in a 2D environment  
Video example:
![gif funzionamento](https://github.com/fabiogueunige/RT1_Assignment1/blob/readRes/resources/AssVideo.mp4) cambia giph

Installing and running
----------------------

The simulator requires a Python 2.7 or Python 3 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## How to Install

To **run** this code you have to follow a few of steps:
* clone the repository
  ```bash
  $ git clone https://github.com/fabiogueunige/RT1_Assignment1.git
  ```
* move inside robot-sim folder 
 ```bash
  $ cd robot-sim/
  ```
* run the code:
  ```bash
  $ python3 run.py assignment.py 
  ```

Usage
--------------------------------

You can download the package and make all your changes (this is the [Licence](https://github.com/fabiogueunige/RT1_Assignment1/blob/main/robot-sim/LICENSE.md) for the distribution.

To **run** all your scripts use run.py before your node-name file, as follow:
```bash
$ python3 run.py <node_fle>
```

Contribution
--------------------------------

Please, do not push changes to this project, but if you want you are free to download it.  
The actual organization is composed by two branches:
* main -> There are all the files necessary for the environment and the Robot operation.
* readRes -> All the resources for the Readme construction.

## Possible Improvements

There are several improvements that can be made to the project such as:
* environment changes: Create a more randomic environment and a more randomic starting position for the Robot
* functions: New possible function for different situations like:
* * wall escaping: Escape from a wall of the arena when the Robot is stuck (understand also when it is really stuck)
  * 
