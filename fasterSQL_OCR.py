import pytesseract as tess
import cv2, os
import sizes
ft = sizes.p2403
mydata = []
import os
path = os.path.join(os.getcwd()+'/generated_SOF')
images = os.listdir(path)
import sqlite3
conn = sqlite3.connect('OCRdatabase.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS textElements (
Image_name text,
Customer_name text,
CNIC text,
Mobile text,
Email text,
Order_Number text
)""")
c.execute("SELECT  * FROM textElements")
checklist = [f[5] for f in c.fetchall()]
config = '-l eng --psm 6 -c tessedit_char_whitelist=" -_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.0123456789@"'
for image in images:
    img = cv2.imread(os.path.join(path,image), 1)
    img = cv2.resize(img, (1700,2400))
    orderID =  img[ft[4][0][1]:ft[4][1][1],ft[4][0][0]:ft[4][1][0]]
    cv2.imshow("im", orderID)
    cv2.waitKey(0)
    ID = tess.image_to_string(orderID, config=config).strip()
    ID = ID.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
    if ID in checklist: continue
    for regionIndex, r in enumerate(ft):
        cropped = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
        textoutput = tess.image_to_string(cropped, config=config).strip()
        textoutput.replace(',', '').replace('.', '').replace('  ','').replace('\n', ' ')
        mydata.append(textoutput)
        print(textoutput)
    c.execute("INSERT INTO textElements VALUES (?, ?, ?, ?, ?, ?)", (image, *mydata))
    mydata = []
conn.commit()
conn.close()
