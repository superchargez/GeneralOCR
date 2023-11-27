import cv2, os, re
import pytesseract
from icecream import ic
import corrections
imgdir = r"C:\Users\jawad\Downloads\projects\ocr\images\new"

region_date_comments = [[(596, 339), (930, 429), 'Field', 'Date and Comments']]
region_date_replies = [[(180, 146), (428, 221), 'Field', 'Date']]
config='--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,_ @"'


def dator():
    # global image_counter
    for img_name in os.listdir(imgdir):
        if img_name.endswith(('c.png', 'r.png')):
            img = cv2.imread(os.path.join(imgdir, img_name), 0)
            if img_name.endswith('r.png'):
                region = region_date_replies
            else: region = region_date_comments
            for region in region:
                region = img[region[0][1]:region[1][1], region[0][0]:region[1][0]]
                text = pytesseract.image_to_string(region, config=config)
                if img_name.endswith('r.png'):
                    dict = corrections.corrected_date(text)
                else:
                    dict = corrections.corrected_date_comments(text)
                ic(dict)
                cv2.imshow('Image', region)
                cv2.waitKey(0)

if __name__ == "__main__":
    dator()