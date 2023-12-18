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

        if move == "X": 
            face_nums = [0, 2]
            
            f = [1, 5, 3, 4]
            
            p = faces[f[0]].copy()
            
            for i in range(3):
                if i == 2: 
                    faces[3][0] = faces[4][3]
                    faces[3][1] = faces[4][2]
                    faces[3][2] = faces[4][1]
                    faces[3][3] = faces[4][0]
                elif i + 1 == 2: 
                    faces[5][0] = faces[3][3]
                    faces[5][1] = faces[3][2]
                    faces[5][2] = faces[3][1]
                    faces[5][3] = faces[3][0]
                    
                else: 
                    faces[f[i]] = faces[f[i+1]].copy()
            
            faces[f[3]] = p

        if move == "Y": 
            face_nums = [4, 5]

            f = [1, 2, 3, 0]
            
            p = faces[f[0]].copy()
            
            for i in range(3):
                faces[f[i]] = faces[f[i+1]]
            
            faces[f[3]] = p

        if move == "Z": 
            face_nums = [1, 3]
            
            f = [2, 4, 0, 5]
            
            p = faces[f[0]].copy()

            for i in range(3):
                faces[f[i]][0] = faces[f[i+1]][2]
                faces[f[i]][1] = faces[f[i+1]][0]
                faces[f[i]][2] = faces[f[i+1]][3]
                faces[f[i]][3] = faces[f[i+1]][1]

            faces[f[3]][0] = p[2]
            faces[f[3]][1] = p[0]
            faces[f[3]][2] = p[3]
            faces[f[3]][3] = p[1]

            
        for face_num in face_nums: 
            if face_num == 3 or face_num == 0: 
                temp = faces[face_num][2]
                
                faces[face_num][2] = faces[face_num][0]
                faces[face_num][0] = faces[face_num][1]
                faces[face_num][1] = faces[face_num][3]
                faces[face_num][3] = temp

            else: 
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
        
        faces = rotateCube(move[0], faces, int(move[1]))

    return faces

def process(move_list): 

    for i in range(len(move_list)): 

        if len(move_list[i]) == 1: 
            move_list[i] += "1"

        if move_list[i][1] == "'": 
            move_list[i] = move_list[i][0] + "3"


def solveTB(queue):

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

m = "F' R2 F' U2 R F2 R2 U2 F'".split(" ")
process(m)

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

    result, cube = solveTB(queue)

if checkSolvedRL(cube): 
    #orient cube so solved faces are on top and bottom
    result.append("Z1")
    cube = rotateCube("Z", cube, 1)
    
elif checkSolvedFB(cube):
    #orient cube so solved faces are on top and bottom
    result.append("X1")
    cube = rotateCube("X", cube, 1)

#both layers solved
if (cube[0][2] == cube[0][3] and cube[1][2] == cube[1][3] and cube[2][2] == cube[2][3] and cube[3][2] == cube[3][3]) and (cube[0][0] == cube[0][1] and cube[1][0] == cube[1][1] and cube[2][0] == cube[2][1] and cube[3][0] == cube[3][1]): 
    pass
#bottom layer solved
elif cube[0][2] == cube[0][3] and cube[1][2] == cube[1][3] and cube[2][2] == cube[2][3] and cube[3][2] == cube[3][3]: 
    #bar on top layer
    if cube[0][0] == cube[0][1] or cube[1][0] == cube[1][1] or cube[2][0] == cube[2][1] or cube[3][0] == cube[3][1]:
        
        if cube[1][0] == cube[1][1]: 
            result.append("Y1")
            cube = rotateCube("Y", cube, 1)
        elif cube[2][0] == cube[2][1]:
            result.append("Y2")
            cube = rotateCube("Y", cube, 2)
        elif cube[3][0] == cube[3][1]: 
            result.append("Y3")
            cube = rotateCube("Y", cube, 3)

        algorithm = "R U R' U' R' F R2 U' R' U' R U R' F'".split()
    else:
        algorithm = "F R U' R' U' R U R' F' R U R' U' R' F R F'".split()

#top layer solved
elif cube[0][0] == cube[0][1] and cube[1][0] == cube[1][1] and cube[2][0] == cube[2][1] and cube[3][0] == cube[3][1]: 
    #bar on bottom layer
    if cube[0][2] == cube[0][3] or cube[1][2] == cube[1][3] or cube[2][2] == cube[2][3] or cube[3][2] == cube[3][3]:
        if cube[1][2] == cube[1][3]: 
            result.append("Y1")
            cube = rotateCube("Y", cube, 1)
        elif cube[2][2] == cube[2][3]:
            result.append("Y2")
            cube = rotateCube("Y", cube, 2)
        elif cube[3][2] == cube[3][3]: 
            result.append("Y3")
            cube = rotateCube("Y", cube, 3)

        algorithm = "R' U R' U' R' F R2 U' R' U' R U R' F' R2".split()
    else:
        result.append("X2")
        cube = rotateCube("X", cube, 2)

        algorithm = "F R U' R' U' R U R' F' R U R' U' R' F R F'".split()
#bars on both layers
elif (cube[0][2] == cube[0][3] or cube[1][2] == cube[1][3] or cube[2][2] == cube[2][3] or cube[3][2] == cube[3][3]) and (cube[0][0] == cube[0][1] or cube[1][0] == cube[1][1] or cube[2][0] == cube[2][1] or cube[3][0] == cube[3][1]): 
    if cube[0][2] == cube[0][3]: 
        result.append("Y3")
        cube = rotateCube("Y", cube, 3)
    elif cube[2][2] == cube[2][3]:
        result.append("Y1")
        cube = rotateCube("Y", cube, 1)
    elif cube[3][2] == cube[3][3]: 
        result.append("Y2")
        cube = rotateCube("Y", cube, 2)

    if cube[0][0] == cube[0][1]: 
        result.append("U3")
        cube = rotateCube("U", cube, 3)
    elif cube[2][0] == cube[2][1]:
        result.append("U1")
        cube = rotateCube("U", cube, 1)
    elif cube[3][0] == cube[3][1]: 
        result.append("U2")
        cube = rotateCube("U", cube, 2)
    
    algorithm = "R2 U' F2 U2 R2 U' F2".split()

#bar on bottom layer
elif cube[0][2] == cube[0][3] or cube[1][2] == cube[1][3] or cube[2][2] == cube[2][3] or cube[3][2] == cube[3][3]: 
    result.append("Z2")
    cube = rotateCube("Z", cube, 2)

    if cube[0][0] == cube[0][1]: 
        result.append("Y3")
        cube = rotateCube("Y", cube, 3)
    elif cube[2][0] == cube[2][1]:
        result.append("Y1")
        cube = rotateCube("Y", cube, 1)
    elif cube[3][0] == cube[3][1]: 
        result.append("Y2")
        cube = rotateCube("Y", cube, 2)
    
    algorithm = "R U' R F2 R' U R'".split()

#bar on top layer
elif cube[0][0] == cube[0][1] or cube[1][0] == cube[1][1] or cube[2][0] == cube[2][1] or cube[3][0] == cube[3][1]: 
    if cube[0][0] == cube[0][1]: 
        result.append("Y3")
        cube = rotateCube("Y", cube, 3)
    elif cube[2][0] == cube[2][1]:
        result.append("Y1")
        cube = rotateCube("Y", cube, 1)
    elif cube[3][0] == cube[3][1]: 
        result.append("Y2")
        cube = rotateCube("Y", cube, 2)
    
    algorithm = "R U' R F2 R' U R'".split()

else: 
    algorithm = "R2 F2 R2".split()

process(algorithm)
cube = scramble(algorithm, cube)
result.extend(algorithm)

#auf
if not checkSolved(cube): 
    if cube[1][0] == cube[0][2]:
        result.append("U1")
        cube = rotateCube("U", cube, 1)
    elif cube[2][0] == cube[0][2]: 
        result.append("U2")
        cube = rotateCube("U", cube, 2)
    elif cube[3][0] == cube[0][2]: 
        result.append("U3")
        cube = rotateCube("U", cube, 3)

print(f"\nmoves: {len(result)}\nsolution: {' '.join(result)}\nfaces: {cube}\ntime: {round(time.time() - sTime, 2)}s\n")
    
#print(faceColours)
#print(curFace)
#print(faceColours[curFace])
#print(quadColours)
