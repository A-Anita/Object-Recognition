import cv2
import numpy as np

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from tkinter import *


root = Tk()
root.withdraw()

showinfo(title='Open',message=f"Selct Original Video")
root.update()
original_file_path=fd.askopenfilename()

root.quit()
root.destroy()
cap = cv2.VideoCapture(original_file_path)
ret,frame=cap.read()
x,y,w,h = cv2.selectROI(frame)
track_window = (x, y, w, h)
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
while(1):
   ret, frame = cap.read()
   if ret == True:
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
       dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
       ret, track_window = cv2.CamShift(dst, track_window, term_crit)
       pts = cv2.boxPoints(ret)
       pts=np.int0(pts)
       img2 = cv2.polylines(frame, [pts], True, 255,2)
       cv2.imshow('img2',img2)
       k = cv2.waitKey(30) & 0xff
       if k == 27:
           break
   else:
       break
cv2.destroyAllWindows()
