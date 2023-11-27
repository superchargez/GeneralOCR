import cv2, os
import pytesseract, logo_matcher
from icecream import ic
import corrections
imgdir = r"C:\Users\jawad\Downloads\projects\ocr\images\new"
regions_sources_replies =[[(580, 227), (760, 293), 'Field', 'Sources'], [(1188, 704), (1305, 769), 'Field', 'Replies']]
config='--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,_ @"'

def detor():
    for img_name in os.listdir(imgdir):
        if img_name.endswith('r.png'):
            img = cv2.imread(os.path.join(imgdir, img_name), 0)
            for region_info in regions_sources_replies:
                region = img[region_info[0][1]:region_info[1][1], region_info[0][0]:region_info[1][0]]
                text = pytesseract.image_to_string(region, config=config)
                logo_name = logo_matcher.logo_match(region)
                platform_name = os.path.splitext(logo_name)[0]
                if region_info[3]=='Sources':
                    source_name = corrections.corrected_source(text)
                    text = platform_name +" " + source_name
                ic(text)
                cv2.imshow('Image', region)
                cv2.waitKey(0)

if __name__ == "__main__":
    detor()
