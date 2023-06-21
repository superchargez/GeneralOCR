import pytesseract
from PIL import Image
import os
import matplotlib.pyplot as plt
import sqlite3
import re
import sizes
save_folder_path = 'sof_test/parts'

def ocr_on_image(image_path, sections, save_folder_path):
    image = Image.open(image_path)
    image = image.convert('L')
    image = image.resize((990, 1400))
    data = []
    for i, section in enumerate(sections):
        x1, y1 = section[0]
        x2, y2 = section[1]
        cropped_image = image.crop((x1, y1, x2, y2))
        cropped_image.save(os.path.join(save_folder_path, f"{os.path.basename(image_path).split('.')[0]} {section[3]}.jpg"))
        if section[3] in ['Mobile', 'CNIC']:
            text = pytesseract.image_to_string(cropped_image, config='outputbase digits -c tessedit_char_whitelist=0123456789-')
        else:
            text = pytesseract.image_to_string(cropped_image)
        text = ' '.join(text.split())
        if section[3] in ['Order']:
            text = pytesseract.image_to_string(cropped_image, config='outputbase digits -c tessedit_char_whitelist=0123456789-')
        else:
            text = pytesseract.image_to_string(cropped_image)
        text = ' '.join(text.split())
        if section[3] == 'Email':
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            match = re.search(email_pattern, text)
            if match:
                text = match.group()
            else:
                text = ''.join([c for c in text if c.isalnum() or c in ['@', '.', '+', '-', '_']])
        elif section[3] == 'Name':
            text = ''.join([c for c in text if c.isalpha() or c.isspace()])
        data.append(text.strip())
        print(f"{section[3]}: {text}")
        # plt.imshow(cropped_image)
        # plt.title(f"{section[3]}\n\n{os.path.basename(image_path)}")
        # plt.show()
    return data


folder_path = 'resized'
sections = sizes.p1400d
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

for filename in os.listdir(folder_path):
    if (filename.endswith('.jpg') or filename.endswith('.png')) and "SOF" in filename:
        image_path = os.path.join(folder_path, filename)
        c.execute("SELECT * FROM textElements WHERE Image_name=?", (filename,))
        if c.fetchone() is None:
            data = ocr_on_image(image_path, sections, save_folder_path)
            c.execute("SELECT * FROM textElements WHERE Order_Number=?", (data[4],))
            if c.fetchone() is None:
                c.execute("INSERT INTO textElements VALUES (?, ?, ?, ?, ?, ?)", (filename, data[4], data[0], data[1], data[2], data[3]))

# conn.commit()
conn.close()

import sys
print(sys.executable)
