from detector import ObjectDetector
import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-d","--detector",required=True)
#ap.add_argument("-i","--image",required=True)
ap.add_argument("-a","--annotate",default=None)
args = vars(ap.parse_args())

cap = cv2.VideoCapture(0)
detector = ObjectDetector(loadPath=args["detector"])

#imagePath = args["image"]
#image = cv2.imread(imagePath)

while True:
  ret,imagePath=cap.read()
  detector.detect(imagePath,annotate=args["annotate"])       
  if cv2.waitKey(25) & 0xFF == ord("q"):
     cv2.destroyAllWindows()
     break
    
