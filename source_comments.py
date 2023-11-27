import cv2, os, re
import pytesseract, logo_matcher
from icecream import ic
import logo_matcher, corrections
imgdir = r"C:\Users\jawad\Downloads\projects\ocr\images\new"

regions_source_comments = [[(164, 200), (340, 275), 'Field', 'Scources']] # comments
regions_source_replies = [[(576, 224), (762, 292), 'Field', 'Source']] # comments
config='--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,_ @"'
# config="""--psm 6 --oem 3 -c 
# tessedit_char_whitelist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,_ '
# tessid_char_blacklist=@
# """
savedir = os.path.join(imgdir, "saved")

image_counter = 1  # Initialize a counter for image filenames
def source():
    global image_counter
    for img_name in os.listdir(imgdir):
        if img_name.endswith(('c.png', 'r.png')):
            img = cv2.imread(os.path.join(imgdir, img_name), 0)
            if img_name.endswith('r.png'):
                region = regions_source_replies
            else: region = regions_source_comments
            for region in region:
                region = img[region[0][1]:region[1][1], region[0][0]:region[1][0]]
                text = pytesseract.image_to_string(region, config=config)
                # ic(text)
                logo_name = logo_matcher.logo_match(region)
                source_name = corrections.corrected_source(text) # text2source_name
                # Extract the social media platform name from the logo filename
                platform_name = os.path.splitext(logo_name)[0]
                # Extract the source name from the text
                # source_name = re.search(r'Sources\s*(.*)', text).group(1)  # commented out here koz mentioned in corrections
                # Combine the platform name and source name
                # source = f'{platform_name} {source_name}'
                source = platform_name +" " + source_name
                ic(img_name, source)
                # ic(text)
                save_path = os.path.join(savedir, f'image_{image_counter}.png')
                # print(f'Saving image to: {save_path}')
                # cv2.imwrite(save_path, region)
                cv2.imshow('Image', region)
                cv2.waitKey(0)
                # ic(text)
                image_counter += 1
                # return source
    return source

if __name__ == "__main__":
    source()