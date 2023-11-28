import cv2
import os

logos_dir = r"C:\Users\jawad\Downloads\projects\ocr\images\new\logos"

# Load the logos
logos = [cv2.imread(os.path.join(logos_dir, logo_name), 0) for logo_name in os.listdir(logos_dir)]

def logo_match(img):
    # Define the region of the image where you expect the logo to be
    height, width = img.shape
    start_row, end_row = int(height * 0.5), height  # bottom half of the image
    start_col, end_col = 0, int(width * 0.3)  # left 30% of the image

    region = img[start_row:end_row, start_col:end_col]

    best_match_logo_name = None
    best_match_val = 0

    # Perform template matching for each logo
    for logo_name, logo in zip(os.listdir(logos_dir), logos):
        res = cv2.matchTemplate(region, logo, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > best_match_val:
            best_match_val = max_val
            best_match_logo_name = logo_name

    return best_match_logo_name
