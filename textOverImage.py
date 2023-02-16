import numpy as np, os
import cv2
from cv2 import imshow, waitKey
image = cv2.imread('test.png',cv2.IMREAD_UNCHANGED)
positions = [(220,590), (1160, 600), (270, 650), (920, 650), (240, 1240)]
path = r"generated_SOF/"
for i in range(1,5):
    for position in positions:
        cv2.putText(
            image, #numpy array on which text is written
            "Python Examples", #text
            position, #position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX, #font family
            .8, #font size
            (209, 80, 0, 255), #font color
            2) #font stroke
    # imshow('output',output)
    # waitKey(0)
    cv2.imwrite(os.path.join(path, 'output'+str(i)+".png"), image)
