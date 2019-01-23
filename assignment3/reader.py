import subprocess
import os
from threading import Thread
import pandas as pd
import csv

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', None)

path2 = "C:\\Users\\Andy\\Documents\\HCL America\\practice assignments\\assignment3\\platform-tools_r28.0.1-windows\\platform-tools"
path = "C:/Users/Andy/Documents/HCL America/practice assignments/assignment3/platform-tools_r28.0.1-windows/platform-tools/logcat.txt"
f = open(path, mode='w').close()
f = open(path, encoding="utf8")
run = 0
#while f:
#     content = f.readlines()
#     print(content)
import time

#def logcat():
#     subprocess.Popen([f'cd {path2}', 'adb.exe logcat > logcat.txt'], shell=True)
#     print("subprocess called")
#f = subprocess.run(['adb', 'logcat'], stdout=subprocess.PIPE)
#logcat()

def inp():
     a = input()
     return
def writetoCSV(line, t):
     c=['date', 'time', 'BatteryMeterView', 'level', 'status', 'health', 'SignalStrength', 'LTE level']
     df2 = ""
     global run
     if t == 0:
          s = line.split()
          date = s[0]
          ti = s[1]
          battery = s[6]
          level = s[8].split(":")[1]
          status= s[9].split(":")[1]
          health = s[10].split(":")[1]
          df2 = pd.DataFrame([[date, ti, battery, level, status, health, "-", "-"]], columns=c)
     if t == 1:
          s = line.split()
          date = s[0]
          ti = s[1]
          signal = list(map(lambda x: x+ " ", s[8:21]))
          lte = s[23].split("=")[1]
          df2 = pd.DataFrame([[date, ti, "-", "-", "-", "-", signal, lte]], columns=c)
     if run == 1:
          df2.to_csv("output.csv", quoting=csv.QUOTE_NONNUMERIC)
     if run > 1:
          df2.to_csv("output.csv", quoting=csv.QUOTE_NONNUMERIC, header=None, mode="a")
          
def logcat():
     while 1:
          global run
          where = f.tell()
          line = f.readline()
          if not line:
               time.sleep(1)
               f.seek(where)
          elif "BatteryMeterView" in line:
               run+=1
               writetoCSV(line, 0)
               #print(line) # already has newline
          elif "onSignalStrengthsChanged"  in line:
               run+=1
               writetoCSV(line, 1)
               #print(line)
def exceptt():
     try:
          logcat()
     except Exception as e:
          print(e)
          exceptt()

#thread1 = Thread(target = exceptt)
#thread2 = Thread(target = inp)
#thread1.start()
#thread2.start()
#print("finished")
exceptt()
