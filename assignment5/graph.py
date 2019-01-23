import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
types = ["Error", "Fatal Error", "Information", "Dalvikvm", "Warning", "Verbose", "Silent"]

def match(x):
    global types
    for s in types:
        if s[0] == x:
            return s


def graph_side(name, objects, a, title):
    fig, ax = plt.subplots()
    y_pos = np.arange(len(objects))
    people = objects
    performance = a
    error = np.random.rand(len(people))


    ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('frequency')
    ax.set_title(title)
    #plt.figure().canvas.manager.full_screen_toggle()
    plt.show()

def graph_errors(name, types, title):
    t = types
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT NAME FROM LOGS WHERE CODE=?",(types,))
    l = cur.fetchall()
    l = list(map(lambda x: x[0], l))
    a = list(map(lambda x: x[0][0], [cur.execute("SELECT COUNT(*) FROM LOGS WHERE NAME=?",(x,)).fetchall() for x in l]))
    total = sum(a)
    
    combined = list(zip(l,a))
    for i in combined:
        if i[1]/total < 0.01:
            l.remove(i[0])
            a.remove(i[1])

    graph_side(name, l, a, title)
    cur.close()
    con.close()
               
def graph(l, performance, title):
    objects = l
    y_pos = np.arange(len(objects))


#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
#y_pos = np.arange(len(objects))
#performance = [10,8,6,4,2,1]
 
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('frequency')
    plt.title(title)
 
    plt.show()

def graph_data(name, length="N/A"):
    global types
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT CODE FROM LOGS")
    l = cur.fetchall()
    l = tuple(map(lambda x: x[0], l))
    #cur.close()
    #on.close()

#objects = l
#y_pos = np.arange(len(objects))

    a = list(map(lambda x: x[0][0], [cur.execute("SELECT COUNT(*) FROM LOGS WHERE CODE=?",(x,)).fetchall() for x in l]))
    performance = a
    l = list(map(lambda x: match(x), l))
    graph(l, a, 'logcat logs for {} seconds'.format(length))
    cur.close()
    con.close()

def graph_stuff(name, length="N/A"):
    graph_data(name)
    graph_errors(name, "E", "Logcat errors apps")
    graph_errors(name, "W", "Logcal warnings apps")
    graph_errors(name, "I", "Logcat Information")
    graph_errors(name, "V", "Logcat Verbose")
    graph_errors(name, "D", "Logcat Dalvikvm")


def main():

    print("enter name of file you want graphed")
    name = input()
    graph_stuff(name)
    
if __name__ == "__main__" : main()

