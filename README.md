# 2x2-Solver

https://www.youtube.com/shorts/pykEr9slMbM

This is a repository containing information on my Arduino 2x2 Rubik's cube solver 

## Hardware

This 2x2 solver utilizes my computer's webcam to gather data on the 2x2 Rubik's cube sides. It also utilizes an Arduino Uno microcontroller which is connected to a stepper motor and servo motor, which rotate the cube and flip the cube respectively. The program utilizes serial communication between my computer and the Arduino with a USB cable. 

## Design 

The 2x2 solver is made with a stepper motor attached to a cube holder allowing the cube to be rotated along the x-axis and uses a servo motor connected to a flipping arm that hits the cube from the bottom to flip the cube along the y-axis. To perform an actual turn of the 2x2 on just the top half, on the top part of the flipping arm there are 2 beams to hold the top half in place by turning the servo the opposite way to the flipping function while the bottom half is turned by the stepper motor. This combination of flipping and turning allows the 2x2 to be turned on any face.

## Program 

The 2x2 solver algorithm uses 2 separate programs, one on my computer in Python on VS code with another running on the Arduino. The Arduino program waits for serial signals given by the Python program on my computer and using those signals, adjusts the servo and stepper motors to perform turning, rotations, and flipping. The Python program is where the algorithm to solve the cube is created. The program first utilizes the Opencv library to create colour masks of the 4 pieces of every side to find the colour of each piece. The webcam colour information is stored in a 2d array, which represents the cube with each subarray containing the colour of each piece in each face of the cube. The 2d array representation of the cube is manipulated through the rotateCube function which moves the elements of the 2d array using specific Rubik's cube notation as can be seen here (https://ruwix.com/the-rubiks-cube/notation/). For simplicity, only 6 moves are implemented as the other moves can be performed from this set of 6 on the 2x2. The solution to solve the Rubik's cube is in the form of an array of these moves "R", "U", "F", "X", "Y", "Z". The Arduino is sent these individual characters and its program then performs different actions with the motors based on the move. 

## Algorithm to solve the cube

The algorithm to solve the cube is a Python version of the 2x2 speedcubing method Ortega as can be read here (https://kewbz.com/pages/2x2-ortega-method-full-algs-guide)

### First Face

The actual solution to solve the cube starts by solving the first face. The program utilizes a bfs approach to solve the first face performing every possible move in every possible order until it solves the first face. Due to the small size of the 2x2, this brute force is feasible not taking too much time to find a solution. The bfs function returns the sequence of moves to successfully solve the first face in the form of an array that will eventually store the whole solution. 

### Top face and last 2 layers

In order to solve the opposite face of the cube, a long series of if statements is used to check for each of the 7 possible cases and append its corresponding sequence of moves to solve that case to the solution array. Since the solutions utilize the full Rubik's cube notation, I created a function, parseToMachine, to convert the algorithm to all "R", "U", and "F" moves. Following finishing the top face, the 2 last layers are finished in a similar manner checking for all the cases and adding it on to the solution array. 

Once the array containing the solution is completed, it is split and each move is sent to the Arduino to physically turn the cube and solve it. 
