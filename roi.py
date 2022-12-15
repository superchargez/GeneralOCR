import cv2 as cv
from cv2 import imread, resize, waitKey, circle, setMouseCallback, imshow, EVENT_LBUTTONDOWN
import random, os

scale = .3
circles = []
counter = 0
counter2 = 0
point1 = []
point2 = []
myPoints = []
myColor = []

def mousePoints(event, x, y, flags, params):
    global counter, counter2, point1, point2, circles, myColor
    if event == EVENT_LBUTTONDOWN:
        if counter == 0:
            point1 = int(x//scale), int(y//scale)
            counter += 1
            myColor = (random.randint(0, 2)*200, random.randint(0, 2)*200, random.randint(0, 2)*200)
        elif counter ==1:
            point2 = int(x//scale), int(y//scale)
            type_of_field = input('Enter Type ')
            name_of_field = input('Enter Name ')
            myPoints.append([point1, point2, type_of_field, name_of_field])
            counter = 0
        circles.append([x,y, myColor])
        counter2 += 1


path = r'C:\Users\Jawad Mansoor\Documents\pyProjects\ocr\pics\resized'
img = imread(os.path.join(path+'\\'+'jawad SOF.jpg'))

img = resize(img, (0, 0), None, scale, scale)
# cv.namedWindow("Display frame", cv.WINDOW_NORMAL)

while True:
    # Display points
    for x, y, color in circles:
        circle(img, (x, y), 3, color, cv.FILLED)
    imshow("Original Image", img)
    setMouseCallback("Original Image", mousePoints)
    if waitKey(1) & 0xFF == ord('s'):
        print(myPoints)
        break


more_rios = [[(1992, 704), (2060, 752), 'Box', 'Corporate'],
[(2292, 700), (2352, 748), 'Box', 'Individual'],
[(284, 744), (1020, 832), 'Text', 'Name'],
[(1564, 752), (2364, 828), 'Text', 'CNIC'],
[(372, 840), (1032, 916), 'Text', 'Mobile'],
[(1212, 836), (2368, 920), 'Text', 'Email'],
[(436, 916), (1060, 1068), 'Text', 'House'],
[(1188, 1076), (1592, 1200), 'Text', 'City'],
[(1176, 1284), (1232, 1336), 'Box', 'Internet'],
[(1596, 1280), (1648, 1336), 'Box', 'TV'],
[(148, 1476), (200, 1536), 'Box', 'Telephone'],
[(1176, 1516), (1232, 1572), 'Box', 'New'],
[(1676, 1520), (1728, 1576), 'Box', 'Existing'],
[(1280, 1684), (1516, 1740), 'Box', 'Charji'],
[(328, 1656), (1124, 1772), 'Text', 'ID'],
[(464, 1540), (1156, 1632), 'Text', 'Package'],
[(600, 3168), (1452, 3304), 'Text', 'Customer Signature'],
[(1920, 3120), (2376, 3292), 'Text', 'Rep Signature'],
[(50, 1126), (770, 1240), 'Text', 'Order ID'],
[(36, 2153), (810, 2310), 'image', 'Signature']
]
