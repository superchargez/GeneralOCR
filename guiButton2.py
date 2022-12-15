from tkinter import *
import os

root = Tk()
# root.iconbitmap('OIP.ico')
myButton = Button(root, text='click me', padx=20, pady=10)
myButton.pack()

def scan():
    myButton['state'] = DISABLED
    print(os.getcwd())
    os.system("python '/home/julia/Documents/learn/python/tess/OCR_with_DB.py'")
    myLabel = Label(root, text='Scan is complete')
    myLabel.pack()

myButton.configure(command=scan)
print('Scan for images is running')
root.mainloop(0)

