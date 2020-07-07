import numpy as np
import cv2

img = cv2.imread('input.png')

original = img.copy()


refined = np.clip(2.0 * img + (-200), 0, 255).astype(np.uint8)
cv2.imwrite("input_refined.png",refined)
img=cv2.imread("input_refined.png")


gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

image = img.copy()

blurred = cv2.GaussianBlur(gray, (1,1), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilate = cv2.dilate(thresh, kernel , iterations=6)


# Find contours in the image
cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

contours = []

threshold_min_area = 3000
threshold_max_area = 15166

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)

    #print("area: " + str(area))
    #print("x,y,w,h: " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))
    
    if area > threshold_min_area:
    	#print("area: "+ str(area))
    	#print("c: " + str(c) + "\nx,y,w,h")
    	#print(x,y,w,h)
    	cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
    	#contours.append(c)

cv2.imwrite('result2.png',img) 