import mss
import numpy as np
import cv2 as cv
from pynput.keyboard import Key,Controller
import time
import threading


OltTop = cv.imread("train\\fishing\\oltaTop.png",0)
barTop = cv.imread("train\\fishing\\barTop.png",0)
barDown = cv.imread("train\\fishing\\barDown.png",0)
fish = cv.imread("train\\fishing\\fish.png",0)
notice = cv.imread("train\\fishing\\bildirim.png",0)
trash = cv.imread("train\\fishing\\trashbox.png",0)

BAR_TOP_COLOUR = np.array([0, 193, 73, 255])
BAR_DOWN_COLOUR = np.array([1, 101, 33, 255])
BAR_COLUMN = 20
FISH_COLOUR = np.array([151, 96, 2, 255])
FISH_COLUMN = 20
EXC_COLOUR1 = np.array([0, 186, 247, 255])
EXC_COLOUR2 = np.array([0, 249, 251, 255])

def find_topBarY(screen):
    topBarY = -1
    
    for row in range(0,600):
        if screen[row][BAR_COLUMN].tolist() == BAR_TOP_COLOUR.tolist():
            topBarY = row
            break

    return topBarY

def find_downbarY(screen):
    downBarY = -1
    for row in range(599,0,-1):
        if screen[row][BAR_COLUMN].tolist() == BAR_DOWN_COLOUR.tolist():
            downBarY = row
            break
    return downBarY
    
def findFish(screen):
    fishY = -1
    for row in range(0,600):
        if screen[row][FISH_COLUMN].tolist() == FISH_COLOUR.tolist():
            fishY = row
            break

    return fishY
    

      
def CPress(C_time):
    keyboard.press('c')
    time.sleep(C_time)
    keyboard.release('c')
    return


starting_Time = 5
for i in range(starting_Time, 0, -1):
    print(f"Starting in {i} second...")
    time.sleep(1)
print("Starded!")  
keyboard = Controller()

keyboard.press("c")
time.sleep(1)
keyboard.release("c")

with mss.mss() as sct:
    
    
    
    while True:
        notice_monitor = {
               "top":350,
               "left":900,
               "width":150,
               "height":120
               }
        notice_screen = np.array(sct.grab(monitor=notice_monitor))
        notice_screen = cv.cvtColor(notice_screen,cv.COLOR_BGR2GRAY)
        notice_res = cv.matchTemplate(notice_screen,notice,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(notice_res)
        NOTICE_UI = False
        cv.imshow("window",notice_screen)
        if cv.waitKey(27) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break
        if max_val > 0.85:
            print("Fish Found!")
            keyboard.press("c")
            time.sleep(0.1)
            keyboard.release("c")
            NOTICE_UI = True
             
        
        
        
         
        
        
        
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        smallRegion = {}
        TRASH_UI = False
        while NOTICE_UI == True:
            FISHING_UI = True
            
                
            while (FISHING_UI == True):
                time.sleep(2)
                screen = np.array(sct.grab(monitor=monitor))
                screen = cv.cvtColor(screen,cv.COLOR_BGR2GRAY)
                
                res = cv.matchTemplate(screen,OltTop,cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                if (max_val > 0.95):
                    print("Fishing started!")
                    FISHING_UI = False
                    fishing_monitor = {"top": monitor['top'] + max_loc[1], "left": monitor['left'] + max_loc[0], "width": 60, "height": 600}
                else:
                    print("Trash Found!")
                    print("Restarting...\n")
                    time.sleep(2)
                    keyboard.press('c')
                    time.sleep(1.25)
                    keyboard.release('c')
                    NOTICE_UI = False
                    TRASH_UI = True
                    break
            
            if TRASH_UI == True:
                break
            
            barY = 0
            fishY = 0
            prev_fark = 0
            prev_BarY = 550
            
            
            fishing = True
            
            screen = np.array(sct.grab(fishing_monitor))
            
            top_barY = find_topBarY(screen)
            
            down_barY = find_downbarY(screen)
            
            half_barY = 0.5
            
            barLenght = down_barY - top_barY
            barHalf = int(half_barY*barLenght)
            
            while fishing == True:
                screen = np.array(sct.grab(fishing_monitor))
                
                top_barY = find_topBarY(screen)
                if top_barY == -1:
                    down_barY = find_downbarY(screen)
                    if down_barY != -1:
                        top_barY = find_downbarY(screen) - barLenght
                    else:
                        screen_bar = cv.cvtColor(screen, cv.COLOR_RGB2GRAY)
                        res = cv.matchTemplate(screen_bar,barTop,cv.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                        if(max_val > 0.80):
                            topBarY = max_loc[1]
                        else:
                            print("Balık bulunamadı!")
                            
                
                
                
                fishY = findFish(screen)
                if fishY == -1:
                    print("Fishing successfull!")
                    print("Restarting...\n")
                    fishing = False
                    time.sleep(2)
                    keyboard.press('c')
                    time.sleep(1.25)
                    keyboard.release('c')
                    
                barY = top_barY + barHalf
                fark = barY - fishY
                fark_speed = fark - prev_fark
                bar_speed = barY - prev_BarY
                values = {"a":0.5/100,"b":1.5/100,"c":0.9/100}
                
                prev_fark = fark
                prev_BarY = barY
                
                C_time = (values["a"]*fark) + (values["b"]*fark_speed) + (values["c"]*bar_speed)
                if C_time > 0.7:
                    C_time = C_time
                
                if C_time > 0:
                    thr = threading.Thread(target=CPress, args=(C_time,))
                    thr.start()
                
                cv.imshow("window",screen)
                if cv.waitKey(25) & 0xFF == ord("q"):
                    cv.destroyAllWindows()
                    break
            if fishing == False:
                break
            
            
         