import cv2
import numpy as np
im = cv2.imread("C:/Users/trainee2018088/butterfly 24-34/Lesser Gull/9.jpg")
copy = im.copy()

kernel = np.zeros((9,3), dtype=int)
color_vector = np.zeros((27),dtype= int)

c=0
count1=0

def click_and_crop(event, x, y, flags, param):
    
    global c, sum_h, sum_s, sum_v,count,kernel,count1
    
    if event == cv2.EVENT_LBUTTONDOWN:
        count=0
        c = c+1
        for i in range(-1,2):
            for j in range (-1,2):
                kernel[count] = im[y+i][x+j]
                count+=1
                
        min_cost=1560600
        a=0
        for i in range(9):
            cost=0
            
            for j in range(9):
                if(i==j):
                    continue
                cost+=(pow((kernel[i][0]-kernel[j][0]),2)+pow((kernel[i][1]-kernel[j][1]),2)+pow((kernel[i][2]-kernel[j][2]),2))
            if(cost<min_cost):
                min_cost=cost
                #print min_cost
                a=i
        
        color_vector[count1] = kernel[a][0]
        color_vector[count1+1] = kernel[a][1]
        color_vector[count1+2] = kernel[a][2] 
        count1+=3
                
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop ) 


while True:
    
    # display the image and wait for a keypress
    cv2.imshow("image", copy)
    key = cv2.waitKey(1)


    # if the 'c' key is pressed, break from the loop
    if key == ord("c") or c==9:
        
        
        break
       
cv2.destroyAllWindows()       
print ""
for i in range(27):
     print color_vector[i]
print ""

