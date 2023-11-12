import cv2
import pytesseract
import os
from icecream import ic
import re
import wordninja
from spellchecker import SpellChecker

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
spell = SpellChecker()
# Specify the directory containing your images
image_dir = r'images'
save_dir = 'save'
os.makedirs(os.path.join(image_dir, save_dir), exist_ok=True)

regions_rp = [[(1764, 482), (2152, 584), 'Text', 'Time'], [(2208, 706), (2382, 800), 'Text', 'Replies']]
regions_im = [[(2060, 432), (2370, 522), 'Text', 'Comments']]

# Image preprocessing options
preprocess = ['contrast']
config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,'
scale = 2

# Create a dictionary to store the results
results = {}

for filename in os.listdir(image_dir):
    if (filename.endswith('.bmp') or filename.endswith('.png')):
        img = cv2.imread(os.path.join(image_dir, filename), 0)
        
        # Determine which regions to use based on the filename
        if 'im' in filename:
            regions = regions_im
        elif 'rp' in filename:
            regions = regions_rp

        for region in regions:
            top_left, bottom_right = region[0], region[1]
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]  # Extract the region of interest
            
            # Preprocess the ROI
            for method in preprocess:
                if method == 'threshold':
                    _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                elif method == 'contrast':
                    roi = cv2.convertScaleAbs(roi, alpha=2.1, beta=-220)
            
            cv2.imwrite(os.path.join(image_dir, save_dir, f"{filename}_{region[3]}.png"), roi)
            scaled_roi = cv2.resize(roi, (roi.shape[1]*scale, roi.shape[0]*scale), interpolation = cv2.INTER_LINEAR)
            # cv2.imshow("ROI Display", scaled_roi)
            # cv2.waitKey(0)
            text = pytesseract.image_to_string(scaled_roi, config=config)
            
            # Split joined words
            words = wordninja.split(text)
            text = " ".join(words)
            
            # Correct misspelled words
            corrected_words = [spell.correction(word) for word in text.split()]
            ctext = " ".join(corrected_words)
            ic(ctext)#, text)
            date_pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{1,2} \d{4}'
            date = re.search(date_pattern, ctext)
            if date:
                date = date.group()
            else:
                date = None
            # ic(date)
            completed_items_pattern = r'Completed Items (\d+)|Completed it\s?ems (\d+)'
            completed_items = re.search(completed_items_pattern, ctext)
            if completed_items:
                # The first group corresponds to 'Completed Items (\d+)', and the second group corresponds to 'Completed it\s?ems (\d+)'
                # One of them will be None depending on which pattern is matched
                completed_items = completed_items.groups()
                completed_items = [item for item in completed_items if item is not None]
                completed_items = int(completed_items[0])  # Convert the result to an integer
            else:
                completed_items = None
            # ic(completed_items)
            
            replies_pattern = r'Total Replies (\d+)|Total Replies\s?(\d+)'
            replies = re.search(replies_pattern, ctext)
            if replies:
                # The first group corresponds to 'Total Replies (\d+)', and the second group corresponds to 'Total Replies\s?(\d+)'
                # One of them will be None depending on which pattern is matched
                replies = replies.groups()
                replies = [item for item in replies if item is not None]
                replies = int(replies[0])  # Convert the result to an integer
                # ic(replies)
            else: replies = None

            time_pattern = r'(\d+)?\s?(hour|minutes)'
            time_match = re.findall(time_pattern, ctext)
            if time_match:
                hours = 0
                minutes = 0
                for match in time_match:
                    if 'hour' in match[1]:
                        hours = int(match[0])
                    elif 'minutes' in match[1]:
                        minutes = int(match[0])
                total_minutes = hours * 60 + minutes
            else: 
                total_minutes = None
            ic(total_minutes)
            
            # Store the result in the dictionary
            results[filename] = text

print(results)
