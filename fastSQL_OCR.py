#%%
import cv2, easyocr, os
import matplotlib.pyplot as plt
import sizes
ft = sizes.p768
reader = easyocr.Reader(['en'], detector='DB', recognizer = 'Transformer', gpu=False)
mydata = []
import os
path = os.path.join(os.getcwd()+'/generated_SOF')
images = os.listdir(path)
#%%
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
# checklist = list()
c.execute("SELECT  * FROM textElements")
# files = c.fetchall()
# for f in files: checklist.append(f[5])
checklist = [f[5] for f in c.fetchall()]
#%%
for image in images:
    img = cv2.imread(os.path.join(path,image), 1)
    orderID =  img[ft[4][0][1]:ft[4][1][1],ft[4][0][0]:ft[4][1][0]]
    ID = reader.readtext(orderID)[0][1]
    if ID in checklist: continue
    for regionIndex, r in enumerate(ft):
        cropped = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
        textoutput = reader.readtext(cropped)[0][1]
        mydata.append(textoutput)
        print(textoutput)
        # plt.imshow(cropped)
        # plt.show()
    c.execute("INSERT INTO textElements VALUES (?, ?, ?, ?, ?, ?)", (image, *mydata))
    mydata = []
conn.commit()
conn.close()
