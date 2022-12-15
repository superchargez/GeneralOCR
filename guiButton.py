from tkinter import *
import os
root = Tk()
root.iconbitmap("C:\\Users\\Jawad Mansoor\\Documents\\pyProjects\\ocr\\OIP.ico")
myButton = Button(root, text='click me', padx=20, pady=10)
myButton.pack()

main = r"C:\Users\Jawad Mansoor\Documents\pyProjects\ocr"
def scan():
    import sys
    myButton['state'] = DISABLED
    myLabel = Label(root, text='Scan is complete')
    os.system('python "C:\\Users\\Jawad Mansoor\\Documents\\pyProjects\\ocr\\testmain.py"')
    myLabel.pack()

myButton.configure(command=scan)
print('Scan for images is running')
root.mainloop(0)