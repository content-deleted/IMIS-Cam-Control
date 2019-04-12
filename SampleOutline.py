
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def outlineImage(filePath):
    # Select the image to be read
    img = cv.imread(filePath,0)
    #img = cv.imread('iron_uneven.jpg', cv.IMREAD_GRAYSCALE)

    #NEW
    blur = cv.GaussianBlur(img,(11,11),0)
    ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    #http://creativemorphometrics.co.vu/blog/2014/08/05/automated-outlines-with-opencv-in-python/
    #See above link to refine edges using contours
    kernel = np.ones((5,5),np.uint8) #square image kernel used for erosion
    erosion = cv.erode(th, kernel,iterations = 1) #refines all edges in the binary image
    #NEW

    #edges = cv.Canny(img,100,150)
    #edges = cv.Canny(th,140,150)
    edges = cv.Canny(erosion,100,150)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    """
    blurred = cv.GaussianBlur(img, (11,11), 0)
    plt.subplot(121),plt.imshow(blurred,cmap = 'gray')
    plt.title('Blurred Image'), plt.xticks([]), plt.yticks([])
    edges = cv.Canny(blurred,80,100)
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    """

    plt.show()

    return edges


if __name__ == "__main__":
    outlineImage("IMIS_Capture_Icon.png")
