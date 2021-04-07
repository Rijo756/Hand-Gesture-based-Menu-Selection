import cv2
import time
import mediapipe as mp
import numpy as np
from collections import Counter

#custom modules
from daytime import dayntime
from weather import weather_api

class HandSelection:
    def __init__(self):
        #defining hand module
        self.mp_Hand = mp.solutions.hands
        self.hands = self.mp_Hand.Hands(max_num_hands=1) #static_image_mode=False, max_num_hands=2, min_detection_confidence = 0.5,min_tracking_confidence=0.5
        self.mp_draw = mp.solutions.drawing_utils

        #parameters
        self.count = 0 #to count the number of fingers are up
        self.view = 1  #the id of screen in display
        self.country = 0  #the selection from first screen, for using in second screen
        self.dayntime = dayntime() #defining the module to get time and date

    def handcapture(self,img):
        #function to get the landmarks for the hand using mediapipe module
        #  and call the function count to get the number of hands raised.
        
        #changing BGR to RGB
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        #getting the hands from the image using media
        results = self.hands.process(imgRGB)

        #using mediapipe module to draw the landmarks into image
        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:   
                self.mp_draw.draw_landmarks(img,handlms, self.mp_Hand.HAND_CONNECTIONS)
                
                #call the function to count the fingers are up.
                self.count = self.countfinger(handlms)
                #print (self.count)
        else:
             self.count = 0
             
        return self.count

    def display(self,screen,timer,selection):
        #function to display the menu and other feilds according to the screen id
        #     and selection values

        #defining the menulist for each screen
        if self.view == 1:
            menulist = ["1. London", "2. Delhi","3. Berlin","4. Chicago","5. Sydney"]
        elif self.view == 2:
            menulist = ["1. Time", "2. Date","3. Temperature","4. Co-ordinates","5. Go back to main menu"]

        #defining the color for the menu and the selection    
        color = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255)]
        if selection == 0:
            pass
        else:
            color[selection-1] = (255,255,0)

        #display the menu and the message     
        y = 200
        for i in range(len(color)):
            cv2.putText(screen,menulist[i],(350,y),cv2.FONT_HERSHEY_PLAIN,2,color[i],2)
            y = y + 80
        cv2.putText(screen,"Show Okay for "+str(timer)+" seconds to choose selected option",(50,600),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        listplace = ["London","Delhi","Berlin","Chicago","Sydney"]

        #for screen 2 to display the selection from first screen
        if self.view == 2:
            place = "Your Selection: " + listplace[self.country]
            cv2.putText(screen,place,(700,75),cv2.FONT_HERSHEY_PLAIN,1.5,(100,255,100),1)
            cv2.putText(screen,"(Show Okay continuesly to display)",(50,630),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)

        #display the output values for screen two
        if self.view == 2 and selection in [1,2,3,4] and timer == 0:
            place = listplace[self.country]
            #print (place)
            weather = weather_api()
            if selection == 1:
                self.dayntime.set_timezone(place)
                value = "Time: " + self.dayntime.gettime()
                #print (value)
            elif selection == 2:
                self.dayntime.set_timezone(place)
                value = "Date: " + self.dayntime.getdate()
                #print (value)
            elif selection == 3:
                value = "Temperature: " + str(weather.get_temp(place))
                #print (value)
            elif selection == 4:
                value = "Coordinates: " + str(weather.get_coordinates(place))
                #print (value)
            cv2.putText(screen,value,(700,100),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2)
            


    def changeview(self,selection):
        #A function to change the view when the function is called and return the new view
        if self.view == 1:
            self.view = 2
            self.country = selection - 1  #storing the selection from first screen when going to second scteen
        else:
            #for screen2 to screen1 the selection should be 5
            if selection == 5: 
                self.view = 1
        return self.view
            
                
    def countfinger(self,handlms):
        #the function to check the landmarks from each finger and check
        #  whether it is up or down and count the number of fingers which
        #  are up
        count = 0

        #check for okay symbol and return -1 for okay
        ytip = handlms.landmark[4].y
        if ytip < handlms.landmark[8].y and ytip < handlms.landmark[12].y and ytip < handlms.landmark[16].y and ytip < handlms.landmark[20].y and ytip < handlms.landmark[5].y and ytip < handlms.landmark[9].y and ytip < handlms.landmark[13].y and ytip < handlms.landmark[17].y:
            return -1 

        #index finger up or down check
        ytip = handlms.landmark[8].y
        y_inside = handlms.landmark[6].y
        if (ytip < y_inside):
            #print ("index")
            count = count + 1

        #middle finger check
        ytip = handlms.landmark[12].y
        y_inside = handlms.landmark[10].y
        if (ytip < y_inside):
            #print ("middle")
            count = count + 1

        #ring finger check
        ytip = handlms.landmark[16].y
        y_inside = handlms.landmark[14].y
        if (ytip < y_inside):
            #print ("ring")
            count = count + 1

        #pinky finger check
        ytip = handlms.landmark[20].y
        y_inside = handlms.landmark[19].y
        y_middle = handlms.landmark[18].y
        if (ytip < y_inside and ytip < y_middle):
            #print ("pinky")
            count = count + 1

        #thumb check
        xtip = handlms.landmark[4].x
        x_inside = handlms.landmark[2].x

        ytip = handlms.landmark[4].y
        y_inside = handlms.landmark[2].y
        if (xtip > x_inside and ytip < y_inside):
            count = count + 1
            #print ("thumb")

        return count
                

#Defining Webcam as video input
cap = cv2.VideoCapture(1)

#defining the handselection class
H = HandSelection()

#parameters for displaying fps
ptime = 0
ctime = 0

#parameters
prev_count = [0,0,0,0,0,0,0,0,0,0] #to store the last 10 values of the selection including okay
prev_selec = [0,0,0,0,0,0,0,0,0,0] #to store the last 10 values of the selection excluding okay
view = 1 #to store the screen id in display
timer = 3 #to store the timer for the Okay symbol

while True:

    #display screen
    screen = np.zeros((720,1280,3),np.uint8)
    
    #reading from webcam
    success,img = cap.read()

    #passing to the Handselection module and getting the count
    count = H.handcapture(img)

    #storing the last 10 selection values including okay
    for i in range(len(prev_count)-1):
        prev_count[i] = prev_count[i+1]
    prev_count[-1] = count

    #storing the last 10 selection values excluding okay
    if count != -1:
        for i in range(len(prev_selec)-1):
            prev_selec[i] = prev_selec[i+1]
        prev_selec[-1] = count

    #The selection is choosed as the most common count from last 10 items excluding okay.    
    selection = Counter(prev_selec).most_common(1)[0][0]
    #print (selection)

    #The count is choosed as the most common count from last 10 items including okay. 
    count = Counter(prev_count).most_common(1)[0][0]

    #check for the okay symbol and a valid selection to control the timer
    if prev_count[-1] == -1 and selection != 0:
        #if a new okay symbol recognised started the timer 
        if prev_count[-2] != -1:
            start_time = time.time()
            timer = 3
        #continues okay symbols will decrease the timer
        else:
            currtime = time.time()
            #print (currtime - start_time)
            timer = max(0,3 - int(currtime - start_time))
    #timer remains 3 for not okay symbol
    else:
        timer = 3

    #check the timer and then change the screen displayed
    if timer == 0:
        if view == 1 or selection == 5: #for new screen the timer is set to default
            start_time = time.time()
            timer = 3
            prev_selec = [0,0,0,0,0,0,0,0,0,0]  
        view = H.changeview(selection)

    #print (selection,prev_selec)
        
    #to calculate fps
    ctime = time.time()
    fps = 1/(ctime-ptime+0.0001)
    ptime = ctime

    #to display the original captured image
    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
      
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    x,y,z = img.shape
    screen [-x:,-y:,:] = img

    #screen display according to the view and selection
    H.display(screen,timer,selection)

    #show the display screen
    cv2.putText(screen,"FPS: "+str(round(fps)),(10,20),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
    cv2.imshow("Gesture Based Simple Menu",screen)
    cv2.waitKey(1)

    
