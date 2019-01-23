import subprocess
import sys
import os
import time
import sqlite3
import threading
from graph import graph_stuff
#PATH = r"C:\Users\Andy\Documents\HCL America\practice assignments\assignment5\platform-tools_r28.0.1-windows\platform-tools\logcat.txt"
PATH = "C:/Users/Andy/Documents/HCL America/practice assignments/assignment5/platform-tools_r28.0.1-windows/platform-tools/logcat.txt"
run=True
t = open(PATH, "w")
t.close()
f = open(PATH, "r", encoding="windows-1252")

def createFileName():
    t = "test.db"
    name = t
    counter = 1
    while os.path.isfile(name):
        name = str(counter)+"_"+t
        counter+=1
    return name

def logcat(name):
     con = sqlite3.connect(name)
     cur = con.cursor()
     while True:
          global run
          if not run:
              cur.close()
              con.close()
              break
          where = f.tell()
          line = ""
          try:
              line = f.readline()
              #print(line)
          except Exception:
              line = False
              
          if not line:
               time.sleep(1)
               f.seek(where)
          else:
              l = line.split()
              if len(l) > 6:
                  cur.execute("INSERT INTO LOGS (DATE, CODE, NAME, MESSAGE) VALUES (?,?,?,?)", ("{} {}".format(l[0],l[1]), l[4], l[5], "test"))
                  con.commit()
                  #print("{} {} {} {}".format(l[0], l[1], l[4], l[5]))

def create_db(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS LOGS (DATE, CODE, NAME, MESSAGE)")
    cur.close()
    con.close()


name = createFileName()
print("Enter how long program should last in seconds")
t = int(input())
create_db(name)
process = subprocess.Popen('test.bat', stdout=subprocess.PIPE, cwd=r"C:\Users\Andy\Documents\HCL America\practice assignments\assignment5")
logthread = threading.Thread(target=logcat, args=(name,))
logthread.start()
time.sleep(t)
run = False
process.terminate()
graph_stuff(name,length=t)
print("finished")
