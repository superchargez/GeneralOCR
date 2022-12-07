import random
import pandas as pd
import cv2 as cv
from cv2 import resize, waitKey, destroyAllWindows, imread, circle, polylines
from cv2 import COLOR_BGR2RGB, cvtColor, imwrite
import numpy as np
from matplotlib import pyplot as plt
import pytesseract as tess
import os

path_to_exe = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess.pytesseract.tesseract_cmd = path_to_exe
conf ='--psm 6 -l eng -c tessedit_char_whitelist="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/ @."'


roi = [
    [(50, 1126), (770, 1240), 'text', 'Order ID'],
    [(50, 500), (260, 680), 'text', 'Name'],
    [(710, 500), (1050, 655), 'text', 'CNIC'], # perfect for SOF 7
    [(50, 550), (248, 720), 'text', 'Mobile'],
    [(710, 550), (920, 700), 'text', 'Email'],
    # [(36, 2153), (810, 2310), 'image', 'Signature']
    ]

def Border20p(myimage):
    tempVal = cv.copyMakeBorder(myimage, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[255, 255, 255])
    return tempVal

sof_folder = r'C:\Users\Jawad Mansoor\Documents\pyProjects\ocr\sof_test'
myPicList = os.listdir(sof_folder)

if not os.path.isfile('homeCodezOutput.csv'):
    with open('homeCodezOutput.csv', 'a+') as f:
        f.write('ID'+',')
        for i, r in enumerate(roi):
            if i+1 < len(r):
                f.write(str(roi[i][3])+',')
            if i+1 == len(r):
                f.write(roi[i][3]+'\n')
                break

with open('homeCodezOutput.csv') as f:
    l = f.readline()
if len(l) < len(roi): 
    with open('homeCodezOutput.csv', 'a+') as f:
        if 'ID' not in l:
            f.write('ID'+',')
        for i, r in enumerate(roi):
            if i+1 < len(r):
                f.write(str(roi[i][3])+',')
            if i+1 == len(r):
                f.write(roi[i][3]+'\n')
                break

df = pd.read_csv('homeCodezOutput.csv')
dfindex= list(df['ID']) # ided
lengthdfindex = len(dfindex)
checklist = dfindex
counter = 0
config = '-l eng+urd --psm 6 oem 0 -c preserve_interword_spaces=1 tessedit_char_whitelist=" ABCDEFGHIJKLMNOPQRSTUVWXYZ=abcdefghijklmnopqrstuvwxyz-.0123456789:#@"'
for j, y in enumerate(myPicList):
    if y not in checklist:
        if 'SOF' in y:
            if lengthdfindex < 1:
                with open('homeCodezOutput.csv', 'a+') as f:
                    f.write('\n'+ y + ',')
                lengthdfindex+=1
            else:
                with open('homeCodezOutput.csv', 'a+') as f:
                    f.write(y + ',')
            img = cv.imread(sof_folder + "/" + y, 1)
            pixelThreshold = 1100
            myData = []
            resized = resize(img,(1700,2400))
            for regionIndex, r in enumerate(roi):
                cropped = resized[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                result = tess.image_to_data(cropped, output_type='dict')
                
                found = 0    
                for textIndex, d in enumerate(result['text']):
                    if found:
                        break
                    if found < 1 and result['conf'][textIndex]!=-1:
                            char_count = 0
                            if char_count < len(r[3]):
                                for charIndex, char in enumerate(d):
                                    if charIndex < len(r[3]) and char.lower().strip() == r[3][charIndex].lower().strip():
                                            char_count += 1
                                            if char_count > len(r[3])*.5:
                                                found = 1
                                                a,b,h,w = result['left'][textIndex], result['top'][textIndex], result['height'][textIndex], result['width'][textIndex]
                                                roi_field = resized[b+r[0][1]:b+h+r[0][1], a+r[0][0]:w+a+r[0][0]]
                                                # plt.imshow(Border20p(roi_field))
                                                roi_field = Border20p(roi_field)
                                                # plt.title(y+" "+r[3])
                                                # plt.imshow(roi_field)
                                                # plt.show()
                                                if r[3] == 'Order ID':
                                                    roi_field_text = tess.image_to_string(roi_field).strip()
                                                    print(roi_field_text)
                                                    text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                                    text = tess.image_to_string(text_named_roi_field).strip()
                                                    text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                                    if text == '': text = 'empty'
                                                    myData.append(text)
                                                    print(f'text {text}')

                                                if r[3] == 'Name':
                                                    roi_field_text = tess.image_to_string(roi_field).strip()
                                                    print(roi_field_text)
                                                    text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                                    text = tess.image_to_string(text_named_roi_field).strip()
                                                    text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                                    if text == '': text = 'empty'
                                                    myData.append(text)
                                                    print(f'text {text}')

                                                if r[3] == 'CNIC':
                                                    roi_field_text = tess.image_to_string(roi_field).strip()
                                                    print(roi_field_text)
                                                    text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w]
                                                    # text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                                    text = tess.image_to_string(text_named_roi_field).strip()
                                                    text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                                    if text == '': text = 'empty'
                                                    myData.append(text)
                                                    print(f'text {text}')

                                                if r[3] == 'Email':
                                                    roi_field_text = tess.image_to_string(roi_field).strip()
                                                    print(roi_field_text)
                                                    # text_named_roi_field = resized[w+a+r[0][0]: b+r[0][1]-h, w+a+r[0][0]+w+w+w+w+w+w+w+w+w: b+h+r[0][1]]
                                                    text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                                    text = tess.image_to_string(text_named_roi_field).strip()
                                                    text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                                    if text == '': text = 'empty'
                                                    myData.append(text)
                                                    print(f'text {text}')

                                                if r[3] == 'Mobile':
                                                    roi_field_text = tess.image_to_string(roi_field).strip()
                                                    print(roi_field_text)
                                                    # text_named_roi_field = resized[w+a+r[0][0]: b+r[0][1]-h, w+a+r[0][0]+w+w+w+w+w+w: b+h+r[0][1]]
                                                    text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                                    text = tess.image_to_string(text_named_roi_field).strip()
                                                    text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                                    if text == '': text = 'empty'
                                                    myData.append(text)
                                                    print(f'text {text}')
                                                
                                                file_name = y.split('.')[0]
                                                plt.title(file_name+" "+r[3])
                                                plt.imshow(text_named_roi_field)
                                                plt.show()
                                                imwrite(os.path.join(os.getcwd()+'/sof_test/parts/'+file_name+" "+r[3]+'.jpg'), text_named_roi_field)
                                                print(tess.image_to_string(roi_field).strip())
                                                break
                if found < 1:
                    file_name = y.split('.')[0]
                    print(f'{r[3]} not found')
                    myData.append(f'{r[3]} not found')
                    imwrite(os.path.join(os.getcwd()+'/sof_test/parts/'+file_name+" "+r[3]+'.jpg'), cropped)
                    plt.title(f"Named roi_field: {r[3]}")
                    plt.imshow(cvtColor(cropped, cv.COLOR_RGB2BGR))
                    plt.show()
            
            with open('homeCodezOutput.csv', 'a+') as f:
                for i, data in enumerate(myData):
                    if i+2 < len(df.columns):
                        f.write(str(data)+',')
                    else:f.write(str(data))
                f.write('\n')
            counter+=1
