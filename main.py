#import library
#import library for creating GUI
from tkinter import *
import tkinter.ttk as ttk
#import library for handling SQLite database
import sqlite3
# https://www.krazyprogrammer.com/2020/12/how-to-search-data-from-sqlite-in.html
import os
#defining function for creating GUI Layout
conn=sqlite3.connect("OCRdatabase.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS textElements (
Image_name text,
Order_Number text,
Customer_name text,
CNIC text,
Mobile text,
Email text
)""")

def DisplayForm():
    #creating window
    display_screen = Tk()
    #setting width and height for window
    display_screen.geometry("800x200")
    #setting title for window
    display_screen.title("PTCL SOF OCR Database")
    global tree
    global SEARCH
    global myButton
    SEARCH = StringVar()
    #creating frame
    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SUNKEN)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(display_screen, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(display_screen, width=1000)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="SQLite Database SOF Records", font=('verdana', 18), width=600,bg="#1C2833",fg="white")
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('verdana', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)

    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=5, fill=X)
    btn_search = Button(LeftViewForm, text="View All", command=DisplayData)
    btn_search.pack(side=TOP, padx=10, pady=5, fill=X)
    myButton = Button(LeftViewForm, text="Scan", command=Scan)
    myButton.pack(side=TOP, padx=10, pady=5, fill=X)

    #setting scrollbar
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Image_name", "Order_Number", "Customer_name", "CNIC","Mobile","Email"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #setting headings for the columns
    tree.heading('Image_name', text="Image Name", anchor=W)
    tree.heading('Order_Number', text="Order Number", anchor=W)
    tree.heading('Customer_name', text="Custommer Name", anchor=W)
    tree.heading('CNIC', text="CNIC", anchor=W)
    tree.heading('Mobile', text="Mobile", anchor=W)
    tree.heading('Email', text="Email", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=180)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def Scan():
    myButton['state'] = DISABLED
    print(os.getcwd())
    os.system("python fastSQL_OCR.py")

#function to search data
def SearchRecord():
    #checking search text is empty or not
    if SEARCH.get() != "":
        #clearing current display data
        tree.delete(*tree.get_children())
        #open database
        conn = sqlite3.connect('OCRdatabase.db')
        #select query with where clause
        cursor=conn.execute("SELECT * FROM textElements WHERE (Image_name || Order_number || CNIC || Mobile || Email || Customer_name) LIKE?", ('%' + str(SEARCH.get()) + '%',))
        #fetch all matching records
        fetch = cursor.fetchall()
        #loop for displaying all records into GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
#defining function to access data from SQLite database
def DisplayData():
    #clear current data
    tree.delete(*tree.get_children())
    # open databse
    conn = sqlite3.connect('OCRdatabase.db')
    #select query
    cursor=conn.execute("SELECT * FROM textElements")
    #fetch all data from database
    fetch = cursor.fetchall()
    #loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#calling function
DisplayForm()
if __name__=='__main__':
#Running Application
 mainloop()
