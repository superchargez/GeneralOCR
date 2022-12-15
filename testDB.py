import sqlite3
conn = sqlite3.connect("testOCRdatabase.sqlite")
c = conn.cursor()

c.execute("SELECT * FROM textElements")
my_data = c.fetchall()
for d in my_data:
    print(d)
conn.close()