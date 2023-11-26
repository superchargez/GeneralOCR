import cv2
import numpy as np
import os

logos_dir = r"C:\Users\jawad\Downloads\projects\ocr\images\new\logos"
imgdir = r"C:\Users\jawad\Downloads\projects\ocr\images\new\saved"

# Load the logos
logos = [cv2.imread(os.path.join(logos_dir, logo_name), 0) for logo_name in os.listdir(logos_dir)]

for img_name in os.listdir(imgdir):
    img = cv2.imread(os.path.join(imgdir, img_name), 0)

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

    print(f'Best match for {img_name}: {best_match_logo_name}')
    cv2.imshow('img', img)
    cv2.waitKey(0)
