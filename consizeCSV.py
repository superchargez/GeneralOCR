import cv2, easyocr, os, polars as pl
fullSized_textLocation =[[(296, 750), (1023, 850)], [(1570, 750), (2350, 850)], [(380, 843), (1020, 920)], [(1220, 843), (2343, 930)], [(323, 1653), (1053, 1780)]]
reader = easyocr.Reader(['en'], detector='DB', recognizer = 'Transformer', gpu=False)
mydata = []
import os
path = os.path.join(os.getcwd()+'/generated_SOF')
images = os.listdir(path)
already_stored = pl.read_csv('OuteasyOCR.csv')
checklist = list(already_stored[:,-1])
ft = fullSized_textLocation
for image in images:
    img = cv2.imread(os.path.join(path,image), 1)
    orderID =  img[ft[4][0][1]:ft[4][1][1],ft[4][0][0]:ft[4][1][0]]
    ID = reader.readtext(orderID)[0][1]
    if ID in checklist: continue
    for regionIndex, r in enumerate(fullSized_textLocation):
        cropped = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
        textoutput = reader.readtext(cropped)[0][1]
        if regionIndex < 4:
            mydata.append(textoutput+ ",")
        elif regionIndex == 4:
            mydata.append(textoutput)
            mydata.append('\n')
with open('OuteasyOCR.csv', 'a+') as f:
    for i, data in enumerate(mydata):
        f.write(data)
