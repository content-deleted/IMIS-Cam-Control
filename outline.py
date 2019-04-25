
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication,QMessageBox)

# Select the image to be read
#im = cv.imread('iron1.jpg')
#im = cv.imread('iron2.jpg')
#im = cv.imread('iron3.jpg')
#im = cv.imread('iron4.jpg')
#im = cv.imread('iron_offscreen.jpg')
#im = cv.imread('iron_uneven.jpg')

def outlineImage(filePath):
  
  im = cv.imread(filePath)

  #Convert to grayscale
  #img = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
  img = im

  #Save a copy of the original image
  copy = im.copy()
  #cv.imshow('Original Image', copy)
  #cv.waitKey(0)

  #Canny edge detection image...
  #edges = cv.Canny(img,100,150)
  #edges = cv.Canny(th,140,150)
  edges = cv.Canny(img,50,100)
  #cv.imshow('Canny',edges)

  # Get the red channel
  _, _, img = cv.split(img)

  #Apply Gaussian Blur to image
  blur = cv.GaussianBlur(img,(13,13),0)
  #Apply OTSU's threshold to image
  ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
  #cv.imshow('OTSU's thresholding', th)

  #Preparing image for contour extraction...
  #http://creativemorphometrics.co.vu/blog/2014/08/05/automated-outlines-with-opencv-in-python/
  #See above link to refine edges using contours
  kernel = np.ones((5,5),np.uint8) #square image kernel used for erosion

  dilate = cv.dilate(th, None, iterations=30) #dilate, puff out edges
  #dilate for other images, iterations = 5
  #dilate for our image, iterations = 30
  #cv.imshow('dilate', dilate)

  erosion = cv.erode(dilate, kernel,iterations = 10) #refines all edges in the binary image
  #erode for other images, iterations = 1
  #erode for our image, iterations = 1 to 10? same
  #cv.imshow('erode', erosion)

  opening = cv.morphologyEx(erosion, cv.MORPH_OPEN, kernel)
  closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel) #this is for further removing small noises and holes in the image
  #print(cv.findContours(closing,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE))
  im2, contours, hierarchy = cv.findContours(closing,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #find contours with simple approximation
  #cv.imshow('Fig 3', closing) #Figure 3

  #Draw all contours back onto "closing" image
  #cv.drawContours(closing, contours, -1, (150, 150, 150), 3, 8, hierarchy)
  #cv.imshow('FIGURE 3 - ALL CONTOUR', closing)

  #Find contour with the largest area...
  areas = [] #list to hold all areas

  for contour in contours:
    ar = cv.contourArea(contour)
    areas.append(ar)

  max_area = max(areas)
  max_area_index = areas.index(max_area) #index of the list element with largest area

  cnt = contours[max_area_index] #largest area contour

  #cv.drawContours(closing, [cnt], 0, (120, 120, 120), 3, maxLevel = 0)
  #3 is thickness
  cv.drawContours(copy, [cnt], 0, (120, 255, 255), 15, maxLevel = 0)

  #Check if sample is centered
  rows, columns = th.shape

  """
  #Find min/max values
  min_row = float("inf")
  min_col = float("inf")
  max_row = float("-inf")
  max_col = float("-inf")
  for row in range(rows):
      for col in range(columns):
          if(th[row,col] == 255):
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
  """
  leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
  rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
  topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
  bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
                  
  boundary_n = topmost[0]#min_row
  boundary_s = rows-bottommost[0]#max_row
  boundary_e = columns-rightmost[0]#max_col
  boundary_w = leftmost[0]#min_col

  tolerance = 0.1
  row_tolerance = int(rows*tolerance)
  column_tolerance = int(columns*tolerance)

  error = 0
  errorMessage = ""
  low_vert_range = boundary_s - row_tolerance
  high_vert_range = boundary_s + row_tolerance
  low_horiz_range = boundary_w - column_tolerance
  high_horiz_range = boundary_w + column_tolerance

  if(not(boundary_n >= low_vert_range and boundary_n < high_vert_range)):
      error = 1
      errorMessage += "ERROR: Image is not centered vertically.\n"
      if(boundary_n > boundary_s):
          errorMessage += "FIX: Please move the sample North.\n\n"
      else:
          errorMessage += "FIX: Please move the sample South.\n\n"
  if(not(boundary_e >= low_horiz_range and boundary_e < high_horiz_range)):
      error = 1
      errorMessage += "ERROR: Image is not centered horizontally.\n"
      if(boundary_e > boundary_w):
          errorMessage += "FIX: Please move the sample East.\n"
      else:
          errorMessage += "FIX: Please move the sample West.\n"
  if(error):
      print(errorMessage)
      #"""
      # make a new popup
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Critical)

      msg.setText(errorMessage)
      msg.setWindowTitle("Positioning Error")
      #msg.setDetailedText("The details are as follows:")
      msg.setStandardButtons(QMessageBox.Ok)
      msg.setEscapeButton(QMessageBox.Close)
      msg.exec_() 
      #"""

  """
  leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
  righttmost = tuple(cnt[cnt[:,:,0].argmax()][0])
  topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
  bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
  """

  cv.imwrite('contour_edge.png', copy)
  cv.waitKey(0)
  cv.destroyAllWindows()

if __name__ == "__main__":
  app = QApplication([])
  screenResolution = app.desktop().screenGeometry()
  screenWidth = screenResolution.width()
  screenHeight = screenResolution.height()

  outlineImage("Testo.jpg")
