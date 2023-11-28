import cv2, os, pytesseract
import pandas as pd
import corrections, logo_matcher
from config import imgdir, config, savedir, image_counter
from regions import *
from icecream import ic
from regions import replies, comments
import pandas as pd

def process_image(img_name, region_info, correction_function=None):
    temp_dict = {}
    img = cv2.imread(os.path.join(imgdir, img_name), 0)
    region = img[region_info[0][1]:region_info[1][1], region_info[0][0]:region_info[1][0]]
    text = pytesseract.image_to_string(region, config=config)
    if correction_function is not None:
        if correction_function.__name__ == 'corrected_source':
            source_name = corrections.corrected_source(text) # text2source_name
            logo_name = logo_matcher.logo_match(region)
            platform_name = os.path.splitext(logo_name)[0]
            dict = platform_name +" " + source_name
            temp_dict['Source'] = dict
        elif correction_function.__name__ == 'corrected_date_comments':
            date, completed_items = correction_function(text)
            temp_dict['Date'] = date
            temp_dict['Completed Items'] = completed_items
        else:
            dict = correction_function(text)
            temp_dict[region_info[3]] = dict
    else:
        dict = corrections.corrected_replies(text)
        if img_name.endswith('r.png'):
            temp_dict['Replies'] = dict
        else:
            temp_dict['Comments'] = dict
    temp_dict['Image Name'] = img_name
    temp_dict['Image Type'] = 'Replies' if img_name.endswith('r.png') else 'Comments'
    # ic(temp_dict)
    # cv2.imshow('img', region)
    # cv2.waitKey(0)
    return temp_dict

df = pd.DataFrame()
for img_name in os.listdir(imgdir):
    result_dict = {}  # Reset the dictionary for each new image
    if img_name.endswith('r.png'):
        result_dict.update(process_image(img_name, replies[0], corrections.corrected_date_of_replies))
        result_dict.update(process_image(img_name, replies[1], corrections.corrected_source))
        result_dict.update(process_image(img_name, replies[2]))  # No correction function for replies
        result_dict.update(process_image(img_name, replies[3], corrections.corrected_time))
    elif img_name.endswith('c.png'):
        result_dict.update(process_image(img_name, comments[0], corrections.corrected_date_comments))
        result_dict.update(process_image(img_name, comments[1], corrections.corrected_source))
    # Convert the dictionary to a DataFrame and append it to the main DataFrame
    ic(result_dict)
    temp_df = pd.DataFrame(result_dict, index=[0])
    df = pd.concat([df, temp_df], ignore_index=True)

# Set 'Date' as the index and save the DataFrame to a CSV file
df.set_index('Date', inplace=True)
df.to_csv('input.csv')
