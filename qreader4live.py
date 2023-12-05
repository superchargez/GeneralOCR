import cv2
from qreader import QReader

# Initialize QReader
reader = QReader()

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    # Decode QR codes in the frame
    decoded_objects = reader.decode(frame)

    for obj in decoded_objects:
        print("Data:", obj.data)
        print("Position:", obj.position)

    # Display the frame
    cv2.imshow('QR code reader', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
