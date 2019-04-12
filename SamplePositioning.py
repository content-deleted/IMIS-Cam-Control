"""
#Original code below
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('iron.jpg',0)
img = cv2.medianBlur(img,5)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

def checkPosition(imageName):
    # Select the image to be read
    #img = cv2.imread('iron1.jpg',0)
    #img = cv2.imread('iron2.jpg',0)
    #img = cv2.imread('iron3.jpg',0)
    #img = cv2.imread('iron4.jpg',0)
    #img = cv2.imread('iron_offscreen.jpg',0)
    img = cv2.imread(imageName,0)


    # global thresholding
    ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # Otsu's thresholding
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img,(11,11),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)




    ### MY TESTS
    rows, columns = th3.shape
    #print "--Image size--"
    #print "rows:",rows
    #print "columns:", columns

    #Find min/max values
    min_row = float("inf")
    min_col = float("inf")
    max_row = float("-inf")
    max_col = float("-inf")
    for row in range(rows):
        for col in range(columns):
            if(th3[row,col] == 255):
                #Find min values
                if(row < min_row):
                    min_row = row
                elif(col < min_col):
                    min_col = col
                #Find max values
                elif(row > max_row):
                    max_row = row
                elif(col > max_col):
                    max_col = col

    #print "\n--Results--"
    #print "min_row:",min_row
    #print "min_col:",min_col
    #print "max_row:",max_row
    #print "max_col:",max_col

    #Check if image is relatively centered
    #NOTE: Northwest corner is (0,0)
    boundary_n = min_row
    boundary_s = rows-max_row
    boundary_e = columns-max_col
    boundary_w = min_col
    #print "boundary_n:",boundary_n
    #print "boundary_s:",boundary_s
    #print "boundary_e:",boundary_e
    #print "boundary_w:",boundary_w

    row_tolerance = int(rows*.05)
    column_tolerance = int(columns*0.05)
    #print "row_tolerance:",row_tolerance
    #print "column_tolerance:",column_tolerance

    error = 0
    low_vert_range = boundary_s - row_tolerance
    high_vert_range = boundary_s + row_tolerance
    low_horiz_range = boundary_w - column_tolerance
    high_horiz_range = boundary_w + column_tolerance
    #print "low_vert_range:",low_vert_range
    #print "high_vert_range:",high_vert_range
    #print "low_horiz_range:",low_horiz_range
    #print "high_horiz_range:",high_horiz_range

    #print ""

    #low_vert <= n < high_vert
    #low_horiz <= e < high_horiz
    '''
    errorMessage = ""
    if(not(boundary_n >= low_vert_range and boundary_n < high_vert_range)):
        error = 1
        errorMessage += "ERROR: Image is not centered vertically.\n"
        if(boundary_n > boundary_s):
            errorMessage += "FIX: Please move the sample North.\n"
        else:
            errorMessage += "FIX: Please move the sample South.\n"
    if(not(boundary_e >= low_horiz_range and boundary_e < high_horiz_range)):
        error = 1
        errorMessage += "ERROR: Image is not centered horizontally."
        if(boundary_e > boundary_w):
            errorMessage += "FIX: Please move the sample East."
        else:
            errorMessage += "FIX: Please move the sample West."
    if(error):
        # make a new popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText(errorMessage)
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Positioning Error")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
    '''

    
    if(not(boundary_n >= low_vert_range and boundary_n < high_vert_range)):
        error = 1
        print ("ERROR: Image is not centered vertically.")
        if(boundary_n > boundary_s):
            print ("FIX: Please move the sample North.")
        else:
            print ("FIX: Please move the sample South.")
    if(not(boundary_e >= low_horiz_range and boundary_e < high_horiz_range)):
        error = 1
        #print "ERROR: Image is not centered horizontally."
        if(boundary_e > boundary_w):
            print ("FIX: Please move the sample East.")
        else:
            print ("FIX: Please move the sample West.")
    if(not error):
        print ("Image is centered.")

    ### END MY TESTS



    # plot all the images and their histograms
    images = [img, ret1, th1,
              img, ret2, th2,
              blur, ret3, th3]
    titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
              'Original Noisy Image','Histogram',"Otsu's Thresholding",
              'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

    for i in xrange(3):
        plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
        plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
        plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
    plt.show()
    
