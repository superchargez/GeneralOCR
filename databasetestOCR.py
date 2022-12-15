# import important libraries and functions
from csv import reader
import cv2 as cv
from cv2 import resize, COLOR_BGR2RGB, cvtColor, imwrite
from matplotlib import pyplot as plt
import pytesseract as tess
import os
import sqlite3
# create a connection to database and intiate a cursor (something that changes values in cells or entire row of a table)
conn = sqlite3.connect('testOCRdatabase.sqlite')
c = conn.cursor()
# create database with 6 headings (columns)
# c.execute("DROP TABLE IF EXISTS images")
c.execute("""CREATE TABLE IF NOT EXISTS textElements (
Image_name text,
Order_Number text,
Customer_name text,
CNIC text,
Mobile text,
Email text
)""")

# for windows, if tesseract library is not in path environment then use this otherwise ignore
path_to_exe = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess.pytesseract.tesseract_cmd = path_to_exe
# obtained regions of interests from ROI function in other python file
roi = [
    [(50, 1126), (770, 1240), 'text', 'Order'],
    [(50, 500), (260, 680), 'text', 'Name'],
    [(710, 500), (1050, 655), 'text', 'CNIC'], # perfect for SOF 7
    [(50, 550), (248, 720), 'text', 'Mobile'],
    [(710, 550), (920, 700), 'text', 'Email'],
    # [(36, 2153), (810, 2310), 'image', 'Signature']
    ]

def Border20p(myimage):
    """Image processing function"""
    #This will add border
    tempVal = cv.copyMakeBorder(myimage, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=[255, 255, 255])
    return tempVal
# since I keep hopping from linux to windows and computer to computer relevant path must be given for image folder
sof_folder = os.path.join(os.getcwd()+'/sof_test')
# list everything in the folder above
myPicList = os.listdir(sof_folder)
# best configuration that I found for tesseract for this project
config = '-l eng --psm 6 -c tessedit_char_whitelist=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.0123456789@"'

checkfile = list()
c.execute("SELECT  * FROM textElements")
files = c.fetchall()
# print(files)
for f in files:
    # print(f[0])
    checkfile.append(f[0])
# loop through list of items in the folder
for j, y in enumerate(myPicList):
    # check if the image information already exists and only use images with 'SOF' in their name
    if y.split('.')[0] not in checkfile and 'SOF' in y:
            img = cv.imread(sof_folder + "/" + y, 1)
            # pixels calculation will come later in use, when all images are exact same size i.e. printed straight from CRM
            pixelThreshold = 1100
            # this list will contain all data read by tesseract
            myData = []
            # resize image to make calculations easy
            resized = resize(img,(1700,2400))
            # this is the main part of the program, it will read the image and extract the text from it
            # enumerate though RIOs and crop them to save processing time
            for regionIndex, r in enumerate(roi):
                cropped = resized[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                # save text obtained from running tresseract on cropped section
                result = tess.image_to_data(cropped, output_type='dict', config=config)
                # create binary logic to verify if there is at least some text read by tesseract
                found = 0    
                # loop through all obtained results
                for textIndex, d in enumerate(result['text']):
                    # if desired text is found then break loop
                    if found:
                        break
                    # only move further if some text is found, check if confidence is not '-1'
                    if found < 1 and result['conf'][textIndex]!=-1:
                        # create character counter so that even if not all characters are found or are found in different place then it would still work
                        char_count = 0
                        if char_count < len(r[3]):
                            for charIndex, char in enumerate(d):
                                # could mistake capital 'O' with 'o' so eleminate chances of mistakes and stop reading characters when desired charcters are found
                                if charIndex < len(r[3]) and char.lower().strip() == r[3][charIndex].lower().strip():
                                    # increase character count for each matching charater
                                    char_count += 1
                                    # if more than half characters are found then call it a desired word
                                    if char_count > len(r[3])*.5:
                                        found = 1
                                        # get coordinates of found string, it might be longer than the desired word
                                        a,b,h,w = result['left'][textIndex], result['top'][textIndex], result['height'][textIndex], result['width'][textIndex]
                                        # get crop section of image to run OCR on it
                                        roi_field = resized[b+r[0][1]:b+h+r[0][1], a+r[0][0]:w+a+r[0][0]]
                                        roi_field = Border20p(roi_field)
                                        # every ROI has different coordinates for their fields where text is to be found, so everyone is separately treated
                                        if r[3] == 'Order':
                                            # remove unncessary spaces as well as various unprintable characters and even newline characters for the name of the ROI
                                            roi_field_text = tess.image_to_string(roi_field, config=config).strip().replace('\n', ' ')
                                            # the estimated frame of the image where the desired text is to be found
                                            text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                            # remove unncessary spaces as well as various unprintable characters and even newline characters for the value of the ROI
                                            text = tess.image_to_string(text_named_roi_field, config=config).strip()
                                            text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                            # if no text is found then mention that field was empty
                                            if text == '': text = 'empty'
                                            # append the list created above
                                            myData.append(text)
                                            # print(f'{r[3]} {text}')

                                        if r[3] == 'Name':
                                            roi_field_text = tess.image_to_string(roi_field, config=config).strip().replace('\n', ' ')
                                            text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                            text = tess.image_to_string(text_named_roi_field, config=config).strip()
                                            text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                            if text == '': text = 'empty'
                                            myData.append(text)
                                            # print(f'{r[3]} {text}')

                                        if r[3] == 'CNIC':
                                            roi_field_text = tess.image_to_string(roi_field, config=config).strip().replace('\n', ' ')
                                            text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w]
                                            # text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                            text = tess.image_to_string(text_named_roi_field, config=config).strip()
                                            text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                            if text == '': text = 'empty'
                                            myData.append(text)
                                            # print(f'{r[3]} {text}')

                                        if r[3] == 'Email':
                                            roi_field_text = tess.image_to_string(roi_field, config=config).strip().replace('\n', ' ')
                                            # text_named_roi_field = resized[w+a+r[0][0]: b+r[0][1]-h, w+a+r[0][0]+w+w+w+w+w+w+w+w+w: b+h+r[0][1]]
                                            text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                            text = tess.image_to_string(text_named_roi_field, config=config).strip()
                                            text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                            if text == '': text = 'empty'
                                            myData.append(text)
                                            # print(f'{r[3]} {text}')

                                        if r[3] == 'Mobile':
                                            roi_field_text = tess.image_to_string(roi_field).strip()
                                            # text_named_roi_field = resized[w+a+r[0][0]: b+r[0][1]-h, w+a+r[0][0]+w+w+w+w+w+w: b+h+r[0][1]]
                                            text_named_roi_field = resized[b+r[0][1]-h:b+h+r[0][1], w+a+r[0][0]:w+a+r[0][0]+w+w+w+w]
                                            text = tess.image_to_string(text_named_roi_field, config=config).strip()
                                            text = text.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
                                            if text == '': text = 'empty'
                                            myData.append(text)
                                            # print(f'{r[3]} {text}')
                                        
                                        file_name = y.split('.')[0]
                                        # print(file_name)
                                        # plt.title(file_name+" "+r[3])
                                        # plt.imshow(text_named_roi_field)
                                        # plt.show()
                                        imwrite(os.path.join(os.getcwd()+'/sof_test/parts/'+file_name+" "+r[3]+'.jpg'), text_named_roi_field)
                                        break
                # if desired text (that is ROI name) is not found
                if found < 1:
                    # decompose file name into file name and extension, take only the file name
                    file_name = y.split('.')[0]
                    # mention that it was not found
                    # print(f'{r[3]} not found')
                    myData.append(f'{r[3]} not found')
                    # save image section that was to be found but could not be
                    imwrite(os.path.join(os.getcwd()+'/sof_test/parts/'+file_name+" "+r[3]+'.jpg'), cropped)
                    plt.title(f"{y} {r[3]}")
                    plt.imshow(cvtColor(cropped, cv.COLOR_RGB2BGR))
                    plt.show()
            
            c.execute("INSERT INTO textElements VALUES (?, ?, ?, ?, ?, ?)", (file_name, *myData))
conn.commit()

c.execute("SELECT rowid, * FROM textElements")
for row in c:
    # print(c.fetchone())
    print(row)

conn.close()