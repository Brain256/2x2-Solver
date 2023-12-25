#import necessary libraries
import cv2
import time
import numpy as np
from collections import deque
import serial

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

        #print(move_list)
        
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

def solvePBL(result, cube): 
    if checkSolvedRL(cube): 
        #orient cube so solved faces are on top and bottom
        result.append("Z1")
        cube = rotateCube("Z", cube, 1)
    
    elif checkSolvedFB(cube):
        #orient cube so solved faces are on top and bottom
        result.append("X1")
        cube = rotateCube("X", cube, 1)

    algorithm = []
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

    return cube

def parseToMachine(moveList): #turns the generated solution into a solution that the robot can use since the robot can only use X, Y and D moves, assumes that the front of the cube is facing the flipper
    newMoves = []

    for move in moveList: 
        if move[0] == "R": 
            newMoves.extend(f"Y3 X1 D{move[1]} X3 Y1".split())
        elif move[0] == "U": 
            newMoves.extend(f"D{move[1]} Y{move[1]}".split())
        elif move[0] == "F": 
            newMoves.extend(f"X3 D{move[1]} X1".split())
        elif move[0] == "Z": 
            newMoves.extend(f"Y3 X{move[1]} Y1".split()) 
        else: 
            newMoves.append(move)
    
    print(newMoves)

    length = len(newMoves) - 1
    i = 0

    while i < length:
        if newMoves[i][0] == newMoves[i+1][0]:
            num = (int(newMoves[i][1]) + int(newMoves[i+1][1])) % 4

            if num == 0:
                newMoves.pop(i)
                newMoves.pop(i)
                length -= 2
                i -= 1
            else:
                newMoves.pop(i+1)
                newMoves[i] = newMoves[i][0] + str(num)
                length -= 1
                i -= 1

        i += 1


    return newMoves

    
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

faceDisplay = [face_left, face_front, face_right, face_back, face_top, face_bottom]
faceColours = [[], [], [], [], [], []]

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

#0 for orange, 1 for red, 2 for green, 3 for blue, 4 for white, 5 for yellow
quadColours = [0, 0, 0, 0]

for i in range(6): 
    faceColours[i] = quadColours.copy()

startTime = 0
curTime = time.time()

cam = cv2.VideoCapture(0)

beginTime = False
sGenerated = False
result = []

ser = serial.Serial('COM5', 115200)

seq = [['Y1'], ['Y1'], ['Y1'], ['Y2', 'X1'], ['X2'], ['X1, Y2']]

#main loop
while True:
    
    #get an image from pi camera
    res, img = cam.read()

    if not beginTime: 
        startTime = time.time()
        beginTime = True 

    curTime = time.time()
        
    if curTime - startTime > 5:
        if curFace != 6:
            curFace += 1

            for move in seq[curFace-1]: 
                time.sleep(0.5)
                print(move)
                ser.write(move.encode())

                while True: 

                    data = ser.readline().decode('utf-8').rstrip()

                    if data == "done":
                        print("move finished")
                        break
                    
            startTime = time.time()
    
    if curFace != 6: 
    
        # convert from BGR to HSV
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # orange mask
        lower_orange = np.array([7, 90, 172])
        upper_orange = np.array([18, 255, 255])

        o_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)
        
        #create red mask
        lower_red = np.array([0, 110, 155])
        upper_red = np.array([6, 255, 255])
        
        r_mask = cv2.inRange(img_hsv, lower_red, upper_red)
        
        #create green mask
        lower_green = np.array([43, 0, 120])
        upper_green = np.array([88, 255, 255])

        g_mask = cv2.inRange(img_hsv, lower_green, upper_green)
        
        #create blue mask
        lower_blue = np.array([92, 120, 110])
        upper_blue = np.array([110, 255, 255])

        b_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
        
        #create white mask
        lower_white = np.array([0, 0, 120])
        upper_white = np.array([180, 70, 255])

        w_mask = cv2.inRange(img_hsv, lower_white, upper_white)
        
        #create yellow mask
        lower_yellow = np.array([20, 90, 160])
        upper_yellow = np.array([40, 255, 255])

        y_mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
        
        #ORANGE
        o_cont_tl = cv2.findContours(o_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        o_cont_tr = cv2.findContours(o_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        o_cont_bl = cv2.findContours(o_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        o_cont_br = cv2.findContours(o_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #RED
        r_cont_tl = cv2.findContours(r_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        r_cont_tr = cv2.findContours(r_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        r_cont_bl = cv2.findContours(r_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        r_cont_br = cv2.findContours(r_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #GREEN
        g_cont_tl = cv2.findContours(g_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        g_cont_tr = cv2.findContours(g_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        g_cont_bl = cv2.findContours(g_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        g_cont_br = cv2.findContours(g_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #BLUE
        b_cont_tl = cv2.findContours(b_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        b_cont_tr = cv2.findContours(b_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        b_cont_bl = cv2.findContours(b_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        b_cont_br = cv2.findContours(b_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #WHITE
        w_cont_tl = cv2.findContours(w_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        w_cont_tr = cv2.findContours(w_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        w_cont_bl = cv2.findContours(w_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        w_cont_br = cv2.findContours(w_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #YELLOW
        y_cont_tl = cv2.findContours(y_mask[ROI_tl[1]:ROI_tl[3], ROI_tl[0]:ROI_tl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        y_cont_tr = cv2.findContours(y_mask[ROI_tr[1]:ROI_tr[3], ROI_tr[0]:ROI_tr[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        y_cont_bl = cv2.findContours(y_mask[ROI_bl[1]:ROI_bl[3], ROI_bl[0]:ROI_bl[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        y_cont_br = cv2.findContours(y_mask[ROI_br[1]:ROI_br[3], ROI_br[0]:ROI_br[2]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        tl = [o_cont_tl, r_cont_tl, g_cont_tl, b_cont_tl, w_cont_tl, y_cont_tl]
        tr = [o_cont_tr, r_cont_tr, g_cont_tr, b_cont_tr, w_cont_tr, y_cont_tr]
        bl = [o_cont_bl, r_cont_bl, g_cont_bl, b_cont_bl, w_cont_bl, y_cont_bl]
        br = [o_cont_br, r_cont_br, g_cont_br, b_cont_br, w_cont_br, y_cont_br]
        
        max_tl_area = 0
        max_tr_area = 0
        max_bl_area = 0
        max_br_area = 0
        
        for i in range(len(tl)):
            if tl[i]:
                for cont in tl[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_tl_area:
                        max_tl_area = area
                        quadColours[0] = i
                    
                    #print(area)
                        
        for i in range(len(tr)):
            if tr[i]:
                for cont in tr[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_tr_area:
                        max_tr_area = area
                        quadColours[1] = i
                    
                    #print(area)
        
        for i in range(len(bl)):
            if bl[i]:
                for cont in bl[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_bl_area:
                        max_bl_area = area
                        quadColours[2] = i
                    
                    #print(area)
                        
        for i in range(len(br)):
            if br[i]:
                for cont in br[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_br_area:
                        max_br_area = area
                        quadColours[3] = i
                    
                    #print(area)

        faceColours[curFace] = quadColours.copy()
        #img = img_hsv

    
    elif not sGenerated:
        
        sTime = time.time()
        queue = deque([])

        if checkSolved(faceColours):
            print("already solved")
            sGenerated = True
            continue

        elif checkSolvedTB(faceColours) or checkSolvedRL(faceColours) or checkSolvedFB(faceColours): 
            cube = faceColours
        else: 
            for move in moves:
                for i in range(3):
                    queue.append([[move + str(i+1)], faceColours])

            result, cube = solveTB(queue)

        cube = solvePBL(result, cube) 

        print(result)
        
        result = parseToMachine(result)
        #m = solveCube(queue)
        #print(m)

        print(f"\nmoves: {len(result)}\nsolution: {' '.join(result)}\nfaces: {cube}\ntime: {round(time.time() - sTime, 2)}s\n")

        sGenerated = True
    
    elif sGenerated: 

        time.sleep(2)

        for move in result: 
            time.sleep(0.5)
            print(move)
            ser.write(move.encode())

            while True: 

                data = ser.readline().decode('utf-8').rstrip()

                if data == "done":
                    print("move finished")
                    break
        
        print(f"cube solved in {round(time.time() - sTime, 2)}s")
        break
    
        
    img = cv2.rectangle(img, (ROI_tl[0], ROI_tl[1]), (ROI_tl[2], ROI_tl[3]), (0, 255, 255), 4)
    img = cv2.rectangle(img, (ROI_bl[0], ROI_bl[1]), (ROI_bl[2], ROI_bl[3]), (0, 255, 255), 4)
    img = cv2.rectangle(img, (ROI_tr[0], ROI_tr[1]), (ROI_tr[2], ROI_tr[3]), (0, 255, 255), 4)
    img = cv2.rectangle(img, (ROI_br[0], ROI_br[1]), (ROI_br[2], ROI_br[3]), (0, 255, 255), 4)
    
    for faceNum in range(min(curFace+1, 6)):
        for quadNum in range(4):
            face = faceDisplay[faceNum][quadNum]
            index = faceColours[faceNum][quadNum]
            
            img = cv2.rectangle(img, (face[0], face[1]), (face[2], face[3]), colCodes[index], -1)
            img = cv2.rectangle(img, (face[0], face[1]), (face[2], face[3]), (0, 0, 0), 1)
        
    #print(faceColours)
    #print(curFace)
    #print(faceColours[curFace])
    #print(quadColours)
    cv2.imshow("image", img)
        
    if cv2.waitKey(1)==ord('q'):
            break
        
cv2.destroyAllWindows()
