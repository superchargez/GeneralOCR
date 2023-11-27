import cv2, os, re
import pytesseract, logo_matcher
from icecream import ic
import corrections
imgdir = r"C:\Users\jawad\Downloads\projects\ocr\images\new"
regions_times_replies = [[(836, 393), (1272, 506), 'Field', 'Time']]
config='--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,_ @"'

def avgtime():
    for img_name in os.listdir(imgdir):
        if img_name.endswith('r.png'):
            img = cv2.imread(os.path.join(imgdir, img_name), 0)
            for region_info in regions_times_replies:
                region = img[region_info[0][1]:region_info[1][1], region_info[0][0]:region_info[1][0]]
                text = pytesseract.image_to_string(region, config=config)
                text = corrections.corrected_time(text)
                cv2.imshow('Image', region)
                cv2.waitKey(0)

if __name__ == "__main__":
    avgtime()
