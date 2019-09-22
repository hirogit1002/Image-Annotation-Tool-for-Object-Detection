import cv2
import PIL
import numpy as np
import os, sys
import json
import re
import sys
from PIL import Image, ImageFilter
image_ptrn = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
image_dir = os.path.join('img' )
images = []
images = [ image for image in os.listdir( image_dir ) if re.match( image_ptrn, image ) ]
output = [ [image_dir+"/"+i] for i in images]
imgs = np.array([np.array(cv2.imread((image_dir+"/"+i))) for i in images])
drawing = False # true if mouse is pressed
ix,iy = -1,-1
x_e,y_e =-1,-1
count =0
k=0
leng = len(imgs)

def callback(event, x, y, flags, param):
    global ix,iy,drawing,img
    if (event == cv2.EVENT_LBUTTONDOWN):
        drawing = True
        ix,iy = x,y
    elif (event == cv2.EVENT_MOUSEMOVE):
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
            a=x
            b=y
            if (a != x | b != y):
                 cv2.rectangle(img,(ix,iy),(x,y),(0,0,0),-1)
    elif (event == cv2.EVENT_LBUTTONUP):
        drawing = False
        if(len(output[count])<2):
            output[count].append(1)
        else:
            output[count][1]+=1
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
        if(x<ix):
            xs = x
            xe = ix
        else:
            xs = ix
            xe = x
        if(y<iy):
            ys = y
            ye = iy
        else:
            ys = iy
            ye = y
        for i in [xs,ys,xe-xs,ye-ys]:
            output[count].append(i)
        print(output[count])
        cv2.imshow("crop",np.array(cv2.imread(image_dir+"/"+images[count]))[ys:ye,xs:xe,:] )
        
def stopper(count,length):
    return (count>=0) and (count<length)
    
cv2.namedWindow('img')
cv2.setMouseCallback('img',callback)
while(stopper(count,leng)):
    img=imgs[count]
    print("count: ",count,"/",leng)
    while(1):
        cv2.imshow("img", img)
        k = cv2.waitKey(1) & 0xFF
        #Escキーを押すと終了
        if (k == 27):
            count =-1
            break
        elif (k == ord('a')):
            count-=1
            break
        elif (k == ord('d')):
            count+=1
            break
        elif (k == ord('r')):
            imgs[count]= np.array(cv2.imread(image_dir+"/"+images[count]))
            output[count] = [image_dir+"/"+images[count]]
            print(output[count])
            break
            
        elif(k ==ord('s')):
            print("Writing")
            str_=""
            with open("info.dat", 'wt') as f:
                for i in output:
                    if(len(i)>1):
                        list_ = [str(x) for x in i]
                        print(list_)
                        str_ += ' '.join(list_) +'\n'
                f.write(str_)
            str_=""
            with open("bg.txt", 'wt') as f:
                for i in output:
                    if(len(i)<2):
                        print(i[0])
                        str_ += i[0] +'\n'
                f.write(str_)
            continue
cv2.destroyAllWindows()
print("End")


