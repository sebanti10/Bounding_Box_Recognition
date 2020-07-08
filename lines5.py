import cv2
import numpy as np

#Function to remove headers and footers.
def boundary(gray):
    edges = cv2.Canny(gray,180,200,apertureSize = 3)
    minLineLength=75
    rows,cols,_= gray.shape
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100, minLineLength=100)
    linevalues=[]
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if(y1!=y2): continue
        linevalues.append(y1)
    linevalues.sort()
    y1bound = max([y for y in linevalues if y<=rows//2])
    y2bound = min([y for y in linevalues if y>=rows//2])
    return y1bound,y2bound


def drawbound():
    image = cv2.imread('input.png')
    image = np.clip(2.0 * image + (-160), 0, 255).astype(np.uint8)
    image1 = image.copy()

    edges = cv2.Canny(image,200,210,apertureSize = 3)
    minLineLength = 150
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges,1,np.pi/180,200,minLineLength,maxLineGap)
    rows,cols,_= image.shape
    line_list=[]
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if(y1==y2):
            line_list.append(y1)
        else:
            continue
    line_list.sort()
    y1_updated = max([y for y in line_list if y<=rows//2])
    y2_updated= min([y for y in line_list if y>=rows//2])


    gray = cv2.cvtColor(image[y1_updated:y2_updated,:],cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (1,1), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilate = cv2.dilate(thresh, kernel , iterations=6)


    cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    contours = []

    threshold_min_area = 3000
    threshold_max_area = 15166

    for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            #if (w>=width-width//2):
            if area > threshold_min_area: 
                cv2.line(image,(x,y1_updated),(x,y+y1_updated), (255,0,0), 2)
                cv2.rectangle(image1, (x, y+y1_updated), (x+w, y+y1_updated + h), (0,255,0), 2)


    cv2.imwrite("result3.png", image1)

drawbound()