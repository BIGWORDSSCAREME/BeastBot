from os import system
from time import sleep
import numpy as np
import cv2

#Cutting the top off of the screenshot image
offset = 580

def stopTap():
    system('stoptap')

def tap(maxLoc, tw, th, sw, sh):
    #My screen is 4096 pixels ig. 0-4096 x and y axis. Have to
    #find ratio for that here and then send tap with the bat file.
    #account for the screenshots crop in the height
    middle = [maxLoc[0] + (tw / 2), maxLoc[1] + offset + (th / 2)]
    taploc = [(middle[0] / sw) * 4096, (middle[1] / sh) * 4096]
    system(f'tap.bat {taploc[0]} {taploc[1]}')

def main():
    #define counter to make program wait for x times to check if the replay
    #button is there
    replaycount = 0

    #defining color of the opposing player in case they cover up the touch blob
    enemycolor = [81, 223, 252]

    #Setup the template for the replay button upon losing
    templatereplay = cv2.imread('goodss/playagain.png')
    #I think its required to cvt to gray not totally sure tho
    templatereplay = cv2.cvtColor(templatereplay, cv2.COLOR_BGR2GRAY)
    trw, trh = templatereplay.shape[::-1]

    #Setup the template for the replay button upon winning
    templatereplayw = cv2.imread('goodss/playagainwin.png')
    templatereplayw = cv2.cvtColor(templatereplayw, cv2.COLOR_BGR2GRAY)
    trww, trwh = templatereplayw.shape[::-1]

    #setup the template for the word "touch" on the blobs to tap
    template1 = cv2.imread('goodss/touch.png')
    template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
    t1w, t1h = template1.shape[::-1]
    
    #Get width and height of screen image
    sShot = cv2.imread('goodss/ss.png')
    SH, SW = sShot.shape[:-1]
    
    while True:
        replaycount = replaycount + 1
        #Check the newest screen shot and convert it to gray
        sShot = cv2.imread('goodss/ss.png')
        #Crop the image to remove the unneeded top portion 
        sShot = sShot[offset:SH, 0:SW]
        sShotColor = sShot
        sShot = cv2.cvtColor(sShot, cv2.COLOR_BGR2GRAY)
        #Find template 1 on the screenshot image
        result = cv2.matchTemplate(sShot, template1, cv2.TM_CCORR_NORMED)
        #get the most/(least?) likely to match the template, the location
        #of the top-left pixel most likely to be a match
        minValue, maxValue, minLoc, maxLoc = cv2.minMaxLoc(result)
        #returns 2 arrays, height first. Searches for enemy color.
        #Have to check if it actually found the color, if not then it
        #Would crash. Even if it doesn't find the color, I believe
        #It returns an array of 2 empty arrays, so have to check those.
        print(maxValue)
        if maxValue < 0.97:
            result = np.where(np.all(sShotColor == enemycolor, axis = 2))
            if len(result[0]) != 0:
                tap([result[1][0], result[0][0]], 75, 75, SW, SH)
        else:
            #Tap if its a good enough match otherwise it could slow the program
            #down.
            tap(maxLoc, t1w, t1h, SW, SH)
        if replaycount > 20:
            #if replaycount is bigger than that number, click replay button, but
            #only if it matches well enough. Takes metaphorical finger off to
            #tap so this could be bad in actual games.
            result = cv2.matchTemplate(sShot, templatereplay, cv2.TM_CCORR_NORMED)
            minValue, maxValue, minLoc, maxLoc = cv2.minMaxLoc(result)
            if maxValue > 0.98:
                #If the game lost play again button is present does this
                stopTap();
                tap(maxLoc, trw, trh, SW, SH)
                stopTap();
                replaycount = 0
                print("replay")
                print(maxValue)
            else:
                #If game lost play again button is not present, checks if game
                #Won button is and if it is executes some stuff.
                result = cv2.matchTemplate(sShot, templatereplayw, cv2.TM_CCORR_NORMED)
                minValue, maxValue, minLoc, maxLoc = cv2.minMaxLoc(result)
                if maxValue > 0.98:
                    stopTap();
                    tap(maxLoc, trww, trwh, SW, SH)
                    stopTap();
                    replaycount = 0
                    print("replay")
                    print(maxValue)
        #sleep()
        #take screenshot and put it in goodss/ss.png
        system(f'ss.bat goodss\ss.png')
        
if __name__ == "__main__":
    main()
