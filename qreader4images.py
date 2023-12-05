from pyzbar.pyzbar import decode
from PIL import Image

def the_answer(img):
    decoded_objects = decode(img)
    return decoded_objects

if __name__ == "__main__":
    image = Image.open('qrcode_test.png')
    decoded_objects = the_answer(image)
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", obj.data.decode('utf-8'))
        print("Position:", obj.rect)
        print("Left:", obj.rect.left)
        print("Top:", obj.rect.top)
        print("Width:", obj.rect.width)
        print("Height:", obj.rect.height)
