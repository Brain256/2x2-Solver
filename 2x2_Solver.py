#import necessary libraries
import cv2
from picamera2 import Picamera2
import time
import numpy as np

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

startTime = time.time()
curTime = time.time()

if __name__ == '__main__':

    #initialize camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640,480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 30
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    #main loop
    while True:
        
        curTime = time.time()
        
        if curTime - startTime > 5:
            if curFace != 5:
                curFace += 1
                startTime = time.time()
                

        #get an image from pi camera
        img = picam2.capture_array()
    
        # convert from BGR to HSV
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # orange mask
        lower_orange = np.array([0, 220, 200])
        upper_orange = np.array([17, 255, 255])

        o_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)
        
        #create red mask
        lower_red = np.array([165, 60, 200])
        upper_red = np.array([180, 255, 255])
      
        r_mask = cv2.inRange(img_hsv, lower_red, upper_red)
        
        #create green mask
        lower_green = np.array([40, 0, 200])
        upper_green = np.array([58, 255, 255])

        g_mask = cv2.inRange(img_hsv, lower_green, upper_green)
        
        #create blue mask
        lower_blue = np.array([89, 60, 200])
        upper_blue = np.array([100, 255, 255])

        b_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
        
        #create white mask
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 35, 255])

        w_mask = cv2.inRange(img_hsv, lower_white, upper_white)
        
        #create yellow mask
        lower_yellow = np.array([28, 240, 160])
        upper_yellow = np.array([34, 255, 255])

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
                        quadColours[0] = colCodes[i]
                    
                    #print(area)
                        
        for i in range(len(tr)):
            if tr[i]:
                for cont in tr[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_tr_area:
                        max_tr_area = area
                        quadColours[1] = colCodes[i]
                    
                    #print(area)
        
        for i in range(len(bl)):
            if bl[i]:
                for cont in bl[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_bl_area:
                        max_bl_area = area
                        quadColours[2] = colCodes[i]
                    
                    #print(area)
                        
        for i in range(len(br)):
            if br[i]:
                for cont in br[i]:
                    area = cv2.contourArea(cont)
                    
                    if area > max_br_area:
                        max_br_area = area
                        quadColours[3] = colCodes[i]
                    
                    #print(area)

        
        
        faceColours[curFace] = quadColours
            
            
        if cv2.waitKey(1)==ord('q'):
            break
        
        
        #cv2.imshow("cam", img)
        #cv2.imshow("blue", b_mask)
        #cv2.imshow("orange", o_mask)
        #cv2.imshow("red", r_mask)
        #cv2.imshow("green", g_mask)
        #cv2.imshow("white", w_mask)
        #cv2.imshow("yellow", y_mask)
        
        img = cv2.rectangle(img, (ROI_tl[0], ROI_tl[1]), (ROI_tl[2], ROI_tl[3]), (0, 255, 255), 4)
        img = cv2.rectangle(img, (ROI_bl[0], ROI_bl[1]), (ROI_bl[2], ROI_bl[3]), (0, 255, 255), 4)
        img = cv2.rectangle(img, (ROI_tr[0], ROI_tr[1]), (ROI_tr[2], ROI_tr[3]), (0, 255, 255), 4)
        img = cv2.rectangle(img, (ROI_br[0], ROI_br[1]), (ROI_br[2], ROI_br[3]), (0, 255, 255), 4)
        
        for faceNum in range(curFace+1):
            for quadNum in range(4):
                face = faceDisplay[faceNum][quadNum]
                colour = faceColours[faceNum][quadNum]
                
                img = cv2.rectangle(img, (face[0], face[1]), (face[2], face[3]), colour, -1)
                img = cv2.rectangle(img, (face[0], face[1]), (face[2], face[3]), (0, 0, 0), 1)
         
        
        cv2.imshow("image", img)
        
        print(faceColours)
        #print(curFace)
        #print(faceColours[curFace])
        #print(quadColours)
        
        
        
    cv2.destroyAllWindows()
