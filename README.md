# What is this project?
<img alt="giphy" width="300" height="300" src="https://user-images.githubusercontent.com/71706645/233994262-664af74d-74c8-40de-98e1-ffdbdfbd6c4d.gif">
This project is based on Jhon Conway's Game of Life. It's a simulator made in python 3.9.1 and pygame 2.3.0.

# But what is 'Life'? :
The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine, meaning that you can create an actual working computer in this simulation. (More about this topic will be shared as I discover)

# Rules of the game:
There are three rules for this game:
1) Any live or filled cell with two or three live neighbours survives.
2) Any dead or 'empty' cell with three live neighbours becomes a live cell.
3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.

# Project dependencies:
- pygame 2.3.0
- pygame_gui 0.6.8

# How to use this simulator:
Run the main.py file after installing the python dependencies.

- Use mouse-left-click to place cells.
- Use mouse-right-click to remove cells.
- Use mouse-middle-button to move around.
- Use 'begin_simulation' to begin the simulation (cells will no longer be editable).
- Use 'stop_simulation' to stop the simulation and edit cells.
- Use 'clear' to remove all the cells

# Explore:
Okay. Theory aside, I believe that what the researcher devised is absoulutely amazing. The thing is turing complete, which means we can build a computer in this simulation. Many people have already done this though. Some people have managed to create the simulation in the simulation. Inception, huh? The possibilities are endless.

Working clock in 'Life':<br>
![image](https://user-images.githubusercontent.com/71706645/233996829-0d43a7b4-8c75-4110-837d-6bdca6eb523c.png)

Working computer in 'Life':<br>
![image](https://user-images.githubusercontent.com/71706645/233997035-e6d507e7-55d8-49b6-858f-790aa1a9473d.png)
