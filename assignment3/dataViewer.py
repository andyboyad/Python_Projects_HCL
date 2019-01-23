import subprocess
import os
from threading import Thread
import pandas as pd
import csv
import time
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', None)
path3 = "C:/Users/Andy/Documents/HCL America/practice assignments/assignment3/platform-tools_r28.0.1-windows/platform-tools/netstats.txt"
path2 = "C:\\Users\\Andy\\Documents\\HCL America\\practice assignments\\assignment3\\platform-tools_r28.0.1-windows\\platform-tools"
path = "C:/Users/Andy/Documents/HCL America/practice assignments/assignment3/platform-tools_r28.0.1-windows/platform-tools/logcat.txt"
#f = open(path, mode='w').close()
#f = open(path, encoding="utf8")
run = 0
#while f:
#     content = f.readlines()
#     print(content)
import datetime

#def logcat():
#     subprocess.Popen([f'cd {path2}', 'adb.exe logcat > logcat.txt'], shell=True)
#     print("subprocess called")
#f = subprocess.run(['adb', 'logcat'], stdout=subprocess.PIPE)
#logcat()

def inp():
     a = input()
     return

def launch_process():
     os.system("start program.bat")
     
def writeData(uid):
     global run
     c = ['date', *uid]
     r = []
     run+=1
     for x in uid:
          i = uid[x]
          s1 = int(i[0].split('=')[1])
          s2 = int(i[1].split('=')[1])
          k = (s1+s2)/1000
          if k > 1000*1000:
               k=round(k/1000000, 2)
               t = str(k)+"GB"
          if k > 1000:
               k=round(k/1000, 2)
               t = str(k)+"MB"
          if k < 1000:
               k=round(k,2)
               t = str(k)+"KB"
          r.append(t)
     df2 = pd.DataFrame([[datetime.datetime.now(), *r]], columns=c)
     if run == 1:
          df2.to_csv("data.csv", quoting=csv.QUOTE_NONNUMERIC)
     if run > 1:
          df2.to_csv("data.csv", quoting=csv.QUOTE_NONNUMERIC, header=None, mode="a")

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

def read_stats():
     p = False
     uid = []
     b = []
     for line in f:
          if "UID stats" in line:
               p = True
          if p:
               if line.split() != []:
                    a = line.split()
                    r = [x for x in a if "rb=" in x or "tb=" in x]
                    u = [x for x in a if "uid=" in x]
                    if r != []:
                         b.append(r)
                    elif u != []:
                         uid.append(u)
          if "UID tag stats" in line:
               p = False
     dic = {x[0]:y for x,y in zip(uid,b)}
     #print(dic)
     writeData(dic)
     #print(**dic)

def readBattery():
     p = False
     for line in f:
          if "Battery History" in line:
               p = True
          if "Statistics since last charge" in line:
               p = True
          if p:
               l = line.split()
               if l != []:
                    print(line)
          if p is True and "1000:" in line:
               p = False
          if p is True and "Per-PID Stats:" in line:
               p = False

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
#exceptt()
for i in range(6*10):
     f = open(path3, encoding="utf8")
     launch_process()
     read_stats()
     f.close()
     time.sleep(1)
