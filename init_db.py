import sqlite3
connection = sqlite3.connect('machines.db')

with open("sqribt.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()
connection.commit()
connection.close()