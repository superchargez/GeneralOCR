import numpy as np, os
import cv2
import randomTextGenerator as gn

positions = [(1581, 835), (290,830), (1223, 915), (390, 914), (330, 1770)]
save_path = r"generated_SOF/"
for i in range(3):
    image_path = r"C:\Users\PTCL\projects\ocr\sof_test\BLANK S OF.jpg"
    image = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)
    texts = gn.gen_texts()
    for j, position in enumerate(positions):
        cv2.putText(
            image, #numpy array on which text is written
            texts[j], #text
            position, #position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX, #font family
            1.7, #font size
            (0, 0, 0, 255), #font color
            2) #font stroke

    cv2.imwrite(os.path.join(save_path, 'output'+str(i)+".png"), image)
