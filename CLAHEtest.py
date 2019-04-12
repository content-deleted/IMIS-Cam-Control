import numpy as np
import cv2
from matplotlib import pyplot as plt

#https://docs.opencv.org/master/d5/daf/tutorial_py_histogram_equalization.html
#Contrast Limited Adaptive Histogram Equalization (CLAHE)

#img = cv2.imread('iron1.jpg',0)
#img = cv2.imread('iron2.jpg',0)
#img = cv2.imread('iron3.jpg',0)
#img = cv2.imread('iron4.jpg',0)
#img = cv2.imread('iron_uneven.jpg',0)
#img = cv2.imread('iron_offscreen.jpg',0)
#img = cv2.imread('IMISStudioSessionTest-040-1.jpg',0)
img = cv2.imread('IMISStudioSessionTest-040-1cut.jpg',0)

# create a CLAHE object (Arguments are optional).
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)

#namedWindow("Display", WINDOW_AUTOSIZE)
#cv2.imshow("Display", cl1)
#cv2.imshow(cl1)
cv2.imwrite('iron_CLAHE.jpg',cl1)

img_CLAHE = cv2.imread('iron_CLAHE.jpg',0)

plt.subplot(1,2,1),
plt.imshow(img, 'gray')
plt.title('ORIGINAL'), plt.xticks([]), plt.yticks([])

plt.subplot(1,2,2),
plt.imshow(img_CLAHE, 'gray')
plt.title('CLAHE'), plt.xticks([]), plt.yticks([])

plt.show()

"""
#plot Threshold and circled Glare
images = [img,img_CLAHE]
titles = ['Original','CLAHE']

for i in range(2):
    plt.subplot(1,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i]), plt.xticks([]), plt.yticks([])
    #plt.subplot(2,2,i*2+1),plt.imshow(images[i*2+1],'gray')
    #plt.title(titles[i*2+1]), plt.xticks([]), plt.yticks([])
plt.show()
"""

