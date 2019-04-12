# import the necessary packages
import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt

"""
#Command line using arpgparse
python GlareDetectAndLabel.py -i iron1.jpg -r 11
python GlareDetectAndLabel.py -i iron2.jpg -r 11
python GlareDetectAndLabel.py -i iron3.jpg -r 11
python GlareDetectAndLabel.py -i iron4.jpg -r 11
python GlareDetectAndLabel.py -i iron_uneven.jpg -r 11
python GlareDetectAndLabel.py -i iron_offscreen.jpg -r 11
"""

"""
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-r", "--radius", type = int,
	help = "radius of Gaussian blur; must be odd")
args = vars(ap.parse_args())
"""

def checkImage(imageName):
    # load the image and convert it to grayscale
    # Select the image to be read
    #image = cv2.imread('iron1.jpg')
    #image = cv2.imread('iron2.jpg')
    #image = cv2.imread('iron3.jpg')
    #image = cv2.imread('iron4.jpg')
    image = cv2.imread(imageName)#'IMIS_Capture_Icon.png')
    #image = cv2.imread('iron_uneven.jpg')
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Set our threshold that says the image has too much glare
    # TO BE FINE TUNED
    myThreshVal = 225

    # Set the radius value for blur
    myRadiusVal = 11

    # the area of the image with the largest intensity value
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    # Check if the largest intensity value is higher than our glare threshold
    if(maxVal > myThreshVal):
        # Circle the area with glare
        cv2.circle(image, maxLoc, 5, (0, 0, 255), 2)
     
    # display the results of the naive attempt
    #cv2.imshow("Naive", image)

    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv2.GaussianBlur(gray, (myRadiusVal, myRadiusVal), 0)

    #
    ret,thr = cv2.threshold(gray,myThreshVal,255,cv2.THRESH_BINARY)
    #ret,thr = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image = thr.copy()
    #cv2.circle(image, maxLoc, args["radius"], (0, 0, 255), 2)
    #cv2.imshow("Filter", image)
    #

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    image = orig.copy()
    #print "maxVal:",maxVal
    cv2.circle(image, maxLoc, myRadiusVal*2+1, (255, 0, 0), 2)

     
    # display the results of our newly improved method
    #cv2.imshow("Robust", image)

    # display original image
    blur = gray.copy()
    #cv2.imshow("Original", blur)

    """
    # plot all the images 
    images = [orig,blur,thr,image]
    titles = ['Original','Blur','Threshold','Glare']

    for i in range(4):
        plt.subplot(1,4,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i]), plt.xticks([]), plt.yticks([])
        #plt.subplot(2,2,i*2+1),plt.imshow(images[i*2+1],'gray')
        #plt.title(titles[i*2+1]), plt.xticks([]), plt.yticks([])
    plt.show()
    """

    #"""
    #plot Threshold and circled Glare
    images = [thr,image]
    titles = ['Threshold','Glare']

    for i in range(2):
        plt.subplot(1,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i]), plt.xticks([]), plt.yticks([])
        #plt.subplot(2,2,i*2+1),plt.imshow(images[i*2+1],'gray')
        #plt.title(titles[i*2+1]), plt.xticks([]), plt.yticks([])
    plt.show()
    #"""
