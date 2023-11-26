#import necessary libraries
import cv2
import time
import numpy as np
from collections import deque

def createFace(x, y, width):
    ROI = [x, y, x + width, y + width]
    
    ROI_tl = [ROI[0], ROI[1], ROI[0] + width/2, ROI[1] + width/2]
    ROI_tr = [ROI[0] + width/2, ROI[1], ROI[0] + width, ROI[1] + width/2]
    ROI_bl = [ROI[0], ROI[1] + width/2, ROI[0] + width/2, ROI[1] + width]
    ROI_br = [ROI[0] + width/2, ROI[1] + width/2, ROI[0] + width, ROI[1] + width]

    ROI_tl = list(map(int, ROI_tl))
    ROI_bl = list(map(int, ROI_bl))
    ROI_tr = list(map(int, ROI_tr))
    ROI_br = list(map(int, ROI_br))
    
    ROI = [ROI_tl, ROI_tr, ROI_bl, ROI_br]
    
    return ROI

def rotateCube(move, faces, times):

    faces = [face.copy() for face in faces]

    for i in range(times): 
        if move == "R":
            face_nums = [2]
            f = [1, 5, 3, 4]
            p1_index = 1
            p2_index = 3
            
            temp1 = faces[1][p1_index]
            temp2 = faces[1][p2_index]
            
            faces[1][p1_index] = faces[5][p1_index]
            faces[1][p2_index] = faces[5][p2_index]
            
            faces[5][p1_index] = faces[3][2]
            faces[5][p2_index] = faces[3][0]
            
            faces[3][2] = faces[4][p1_index]
            faces[3][0] = faces[4][p2_index]
            
            faces[4][p1_index] = temp1
            faces[4][p2_index] = temp2
            
        if move == "U":

            face_nums = [4]
            f = [1, 2, 3, 0]
            p1_index = 0
            p2_index = 1
            
            p1 = faces[f[0]][p1_index]
            p2 = faces[f[0]][p2_index]
            
            for i in range(3):
                faces[f[i]][p1_index] = faces[f[i+1]][p1_index]
                faces[f[i]][p2_index] = faces[f[i+1]][p2_index]
            
            faces[f[3]][p1_index] = p1
            faces[f[3]][p2_index] = p2
        
        if move == "F":
            face_nums = [1]
            
            temp1 = faces[4][2]
            temp2 = faces[4][3]
            
            faces[4][2] = faces[0][3]
            faces[4][3] = faces[0][1]
            
            faces[0][3] = faces[5][1]
            faces[0][1] = faces[5][0]
            
            faces[5][1] = faces[2][0]
            faces[5][0] = faces[2][2]
            
            faces[2][0] = temp1
            faces[2][2] = temp2
            
        for face_num in face_nums: 
            temp = faces[face_num][2]
            
            faces[face_num][2] = faces[face_num][3]
            faces[face_num][3] = faces[face_num][1]
            faces[face_num][1] = faces[face_num][0]
            faces[face_num][0] = temp

    return faces

def checkSolvedTB(faces): 

    for i, face in enumerate(faces): 
        if i == 4 or i == 5: 
            col = face[0]
            for piece in face: 
                if piece != col: 
                    return False

    return True

def checkSolvedRL(faces): 

    for i, face in enumerate(faces): 
        if i == 2 or i == 0: 
            col = face[0]
            for piece in face: 
                if piece != col: 
                    return False

    return True

def checkSolvedFB(faces): 

    for i, face in enumerate(faces): 
        if i == 3 or i == 1: 
            col = face[0]
            for piece in face: 
                if piece != col: 
                    return False

    return True

def checkSolved(faces): 

    for i, face in enumerate(faces): 
            col = face[0]
            for piece in face: 
                if piece != col: 
                    return False

    return True

def scramble(move_list, faces): 

    for move in move_list: 

        if len(move) == 1: 
            move = move + "1"

        if move[-1] == "'": 
            faces = rotateCube(move[0], faces, 3)
            continue
        
        faces = rotateCube(move[0], faces, int(move[1]))

    return faces

def solveCube(queue):

    while len(queue) > 0:
        
        cur = queue.popleft()
        move_list = cur[0]
        faces = cur[1]

        #print(queue)

        if len(move_list) > 11:
            break

        print(move_list)
        
        faces = rotateCube(move_list[-1][0], faces, int(move_list[-1][1]))
        #print(faces)
        
        if checkSolved(faces) or checkSolvedTB(faces) or checkSolvedRL(faces) or checkSolvedFB(faces): 
            return move_list, faces

        for move in moves:
            for i in range(3):
                moveTemp = move_list.copy()
                if move != move_list[-1][0]:
                    moveTemp.append(move + str(i+1))
                    
                    queue.append([moveTemp, faces])

    return []


    
moves = ["R", "U", "F"]
    

ROI_tl = createFace(220, 140, 200)[0]
ROI_tr = createFace(220, 140, 200)[1]
ROI_bl = createFace(220, 140, 200)[2]
ROI_br = createFace(220, 140, 200)[3]

#0 - Left, 1 - front, 2 - right, 3 - back, 4 - top, 5 - bottom
curFace = 0

face_left = createFace(10, 70, 50)
face_front = createFace(70, 70, 50)
face_right = createFace(130, 70, 50)
face_back = createFace(190, 70, 50)
face_top = createFace(70, 10, 50)
face_bottom = createFace(70, 130, 50)

#0 for orange, 1 for red, 2 for green, 3 for blue, 4 for white, 5 for yellow
faceDisplay = [face_left, face_front, face_right, face_back, face_top, face_bottom]
faceColours = [[0, 0, 0, 0], [2, 2, 2, 2], [1, 1, 1, 1], [3, 3, 3, 3], [4, 4, 4, 4], [5, 5, 5, 5]]

colours = ["orange", "red", "green", "blue", "white", "yellow"]

#colour codes in BGR
colCodes = [
    (0, 165, 255),   # Orange
    (0, 0, 255),     # Red
    (0, 255, 0),     # Green
    (255, 0, 0),     # Blue
    (255, 255, 255), # White
    (0, 255, 255)    # Yellow
]

sTime = time.time()

m = "U2 F U' R' F R2 U2 F U'".split(" ")

faceColours = scramble(m, faceColours) 

queue = deque([])

result = []

if checkSolved(faceColours):
    print(queue)
    print("already solved")
else: 
    for move in moves:
        for i in range(3):
            queue.append([[move + str(i+1)], faceColours])

    result, cube = solveCube(queue)

    if result: 
        print(f"moves for solution: {len(result)} \nmoves: {result}\nfaces: {cube}")
    else:
        print("no solution")

'''
if checkSolvedRL(cube): 
    #orient cube so solved faces are on top and bottom
    pass
elif checkSolvedFB(cube):
    #orient cube so solved faces are on top and bottom
    pass

#5 Ortega PBL Algorithms

if bottom layer solved

    if bar present on top layer

        solve for case 1 

    if no bar present

        solve for case 2

elif top layer solved

    -reorient so that top layer is on bottom

    if bar present on top layer

        solve for case 1 

    if no bar present

        solve for case 2

elif 1 bar on both layers

    solve for case 3

elif only 1 bar

    solve for case 4

else

    solve for case 5

'''




print(f"\ntime: {round(time.time() - sTime, 2)}s")
    
#print(faceColours)
#print(curFace)
#print(faceColours[curFace])
#print(quadColours)
