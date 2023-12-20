import cv2
import numpy as  np
import math
import matplotlib.pyplot as plt


def max_distance_points():
    print ("max_distance_points")
   
    w = np.size(im,0)
    h = np.size(im,1)
    dist_max=0
    c0_max = 0
    r0_max = 0
    c1_max = 0
    r1_max = 0
    img1 = np.zeros( np.shape(im) , dtype = "uint8")
    
    im2, contours, hierachy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range (len(contours[0])):
        c0, r0 = contours[0][i][0]
        for j in range(len(contours[0])):
            c1, r1 = contours[0][j][0]
            distance = pow( c0 - c1 , 2) + pow (r0 - r1 , 2)
            if distance > dist_max :
                dist_max = distance
                c0_max = c0
                r0_max = r0
                c1_max = c1
                r1_max = r1
    
                    
    print("1st_point :)", c0_max , r0_max )
    print("2nd_point :)", c1_max , r1_max )
    img1[r0_max][c0_max] = 255
    img1[r1_max][c1_max] = 255
    cv2.imshow("Max_distance_points",img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    xc= (c0_max+ c1_max)/2.0
    yc= (r0_max+ r1_max)/2.0    
    x3 = (0.2 * c0_max + 0.3 * xc)/ 0.5
    y3 = (0.2 * r0_max + 0.3 * yc)/ 0.5
    
    x4 = (0.2 * c1_max + 0.3 * xc)/ 0.5
    y4 = (0.2 * r1_max + 0.3 * yc)/ 0.5
    
                  
    return x3, y3, x4, y4

def area(x3, y3, x4 , y4):
    print ("area")
    x_area = np.zeros( [4], dtype= int)
    y_area = np.zeros( [4], dtype= int)
    x1 = np.size(im,0)
    y1 = np.size(im,1)
    j_index = np.zeros([4], dtype = int)
    img  = np.zeros(np.shape(im), dtype = "uint8")
    y=0
    c1= 0
    c2= 2
    im2, contours, hierachy = cv2.findContours( im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("length_contours" , len(contours[0]))
    a= len(contours[0])
    for i in range(a):
        c0, r0 = contours[0][i][0]
        a = r0 + (1.0 * (x4-x3))/(y4 - y3) * (c0-x3) - y3
        b = r0 +(1.0 * (x4-x3))/(y4 - y3) * (c0-x4) - y4
        if (a * b <= 0 ):
            img[r0][c0] =255 
                        
    cv2.imshow("img2...Curve", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


def curve_min(img):
    print ("curve_min")
    
    global j_min_global
    w = np.size(im , 0)
    h = np.size(im , 1)
    r_min1 = -1
    c_min1 = -1
    r_min0 = -3
    c_min0 = -3
    global j0_min
    im2, contours, hierachy = cv2.findContours( img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
    global j0_min
    dist_min = w *w + h*h
    for i in range (len(contours[0])):
        c0, r0 = contours[0][i][0]
        
        for j in range(len(contours[1])):
            c1, r1 = contours[1][j][0]
            dist = pow(c1 - c0 ,2) + pow(r1 - r0 , 2)
            if dist < dist_min :
                dist_min = dist
                #print("MIn_DIS", dist_min)
                if c1 < c0:
                    r_min0 = r1
                    c_min0 = c1
                else:
                    r_min0 = r0
                    c_min0 = c0
    
    im2 , contours, hh = cv2.findContours(im.copy() , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours[0])):
        c0, r0 = contours[0][i][0]
        if c0 == c_min0 and r0 == r_min0:
            j0_min = i
       
    return     



def span():
    print ("span")
    im2 , contours, hierachy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    n = len(contours[0])
    print("n" , n)
    li  = np.zeros([601], dtype = float )
    s = np.zeros([601], dtype = float )
    index_j = np.zeros([601], dtype = int )
    p_li  = np.zeros([601], dtype = float )
    points = 600
    count =0
    start_array = -1
    start_point = 0
    while( points >0):
        step_size = int(math.ceil(n *1.0 / points))
        print("step_size", step_size)
        for i in range(start_point,n + start_point, step_size):
            k =i
            if k>n:
                k = k - n-1
            index_j[count] = k
            count +=1
            start_point +=1
        print("Count", k)    
        points = math.floor(points - ((n*1.0)/ step_size))
        print("points", points)
    index_j[count] = j0_min
    temp = -1
    for i in range (601):
        for j in range (600- i ): 
            if index_j[j] > index_j[j+1] :
                temp = index_j[j]
                index_j[j] = index_j[j+1]
                index_j[j+1] = temp
    repeat = 0            
    for i in range(601):
        if index_j[i] == j0_min:
            start_array = i
        if i < 599:
            if index_j[i] == index_j[i+1]:
                repeat +=1
                index_j[i+1] = int(index_j[i+1] + index_j[i+2])/2.0
    #print("index_j", index_j)
    #print("repeat", repeat)
    c= 0
    for i in range (start_array, 601 + start_array):
        m = i
        count = 0
        if i > 600:
            m = i -601
        #print("m", m)
        
        x0 , y0 = contours[0][index_j[m]][0]
        for j in range(m+1, (601 + m)) :
            k = j
            if k > 600:
                k = k - 601
            #print("k", k)
            x1 , y1 = contours[0][index_j[k]][0] 
            li[count] = math.sqrt(pow( x1 -x0 , 2) + pow( y1 - y0 , 2))
            count = count +1
            
        #print("li" , li)
        sum_li = sum(li)
        p_li  = (1.0 / sum_li) * np.array(li)
        
        si =0
        for k in range (600) :
            if p_li[k] !=0:
                si += p_li[k] * abs(math.log(p_li[k])) / math.log(600)  
        
        s[c] = si
        c += 1
        
    #print("p_li", p_li)
    return s

def len_prob(li):
    print ("len_prob")
    sum_li = sum(li)
    print(sum_li)
    p_li  = np.zeros([360], dtype = float )
    s = np.zeros([360], dtype = float )
    s_max = 0
    for i in range(0,360):
        p_li[i] = li[i]* 1.0 / sum_li
        
            #print("j", j , p_li[j])
        s[i] = 1.0 * p_li[i] * abs(math.log(p_li[i]))/ math.log(360)
        s[i]=sum(s)
    s_min=s[0]
    s_max=s[359]
       
            
    
    for i in range(360):
        s[i] = (s[i] - s_min) * 1.0 / ( s_max - s_min)
        
    return s
                        
 
refPt = np.zeros([300, 2], dtype = int) 
cropping = False
c =0
image = cv2.imread("C:/Users/trainee2018088/butterfly 24-34/Gram Blue(Ventral)/10.jpg")
copy = image.copy()
mask = np.zeros( np.shape(copy) , dtype = "uint8" )



def click_and_crop(event, x, y, flags, param):
    
    global refPt, cropping, c
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt[c][0] = x
        refPt[c][1] = y
        c = c+1
        cropping = True
        
    if c>2:
        arr = refPt[0: c]
        cv2.fillPoly(mask, [arr] ,  (255, 255, 255))
        cv2.fillPoly(copy, [arr] ,  (255, 255, 255))
  
        
    
    return
print("1")
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop )            

while True:
    
    # display the image and wait for a keypress
    cv2.imshow("image", copy)
    key = cv2.waitKey(1)


    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        copy = image.copy()
        refPt = np.zeros([300, 2], dtype = int)
        mask = np.zeros( np.shape(copy) , dtype = "uint8" )
        c=0

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        print("2")
        break
        
        
cv2.imshow("Mask", mask)
cv2.waitKey(0)
        


im = mask.copy()
im = cv2.Canny(im , 240, 255)
im2 , contours , h = cv2.findContours(im , cv2.RETR_LIST , cv2.CHAIN_APPROX_NONE)
print("Length of contours", len(contours))

cv2.imshow("Canny",im)
cv2.waitKey(0)
cv2.destroyAllWindows()

x3, y3, x4, y4 = max_distance_points()
print("max distance points",x3, y3, x4, y4)
img = area(x3, y3, x4, y4)
curve_min(img)
#print("SEE",abs_c_centre, abs_r_centre)
s =span()

i_array = np.zeros([601] , dtype = int)
for i in range(601):
    i_array[i] = i 
plt.plot(i_array, s)    
#s =len_prob(li)
#print(s)
for i in range(601):
    print(s[i])
    

