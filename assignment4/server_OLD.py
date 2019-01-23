from flask import Flask, render_template, session, redirect, url_for, request, flash, send_from_directory, send_file
app = Flask(__name__)
from random import randint
import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename
import os
import os.path
import time
from pathlib import Path
#UPLOAD = 'C:\\Users\\Andy\\Documents\\HCL America\\practice assignments\\assignment4\\uploads'
UPLOAD = open('upload_dir.txt').read()
app.config['UPLOAD_FOLDER'] = UPLOAD
name = "cool.db"

con = ""
def generate_random():
    l = [chr(randint(97,122)) for i in range(30)]
    return "".join(l)

def delete_id(ID):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur = cur.execute("SELECT * FROM FILES WHERE ID=?", (ID,))
    data = cur.fetchall()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data[0][1]))
    print("File Removed!")
    cur.execute("DELETE FROM FILES WHERE ID=?", (ID,))
    con.commit()
    cur.close()
    con.close()

def download_from_id(ID):
    print("should have worked")
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("SELECT * FROM FILES WHERE ID=?", (ID,))
    data = cur.fetchall()
    cur.close()
    con.close()
    if not data:
        return []
    return data[0]
   # return send_from_directory(app.config['UPLOAD_FOLDER'],
     #                          data[0][1])

def tests(ID):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("SELECT * FROM FILES WHERE ID=?", (ID,))
    data = cur.fetchall()
    print(data[0][0])
    cur.close()
    con.close()

@app.route('/file/<ID>')
def get_file(ID):
    d = download_from_id(ID)
    print(d)
    if not d:
        return "File not found"
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], d[1]), as_attachment=True)

@app.route('/download/<ID>')
def download(ID):
    d = download_from_id(ID)
    print(d)
    if not d:
        return "File not found"
    return render_template("download.html", ID=d[0], name=d[1], size=d[2], size2 = round(d[2]/1000), size3 = round(d[2]/1000000))
    #print(d)
    #return send_file(os.path.join(app.config['UPLOAD_FOLDER'], d), as_attachment=True)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
     #                          d)
#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'],
#                               filename)


#@app.route('/success')
#def success():
#    return render_template("success.html")


@app.route('/delete/<ID>')
def delete(ID):
    d = download_from_id(ID)
    if not d:
        return "File does not exist"
    delete_id(ID)
    return render_template("delete.html", name=d[1])

@app.route('/', methods=['POST'])
def upload():
    
    file = request.files['file']
    print(file)
    if file == "0":
        return redirect(request.url)
    if not file:
        return redirect(request.url)
    if 'file' not in request.files:
        return redirect(request.url)
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        #file.save(app.config['UPLOAD_FOLDER']+"/"+filename)
        filename = file_checker(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        g = save_file(filename)
        return render_template('success.html', ID=g)
        #return redirect('/success')
        #return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')
    
@app.route('/', methods=['GET'])
def hello():
    print(session)
    return render_template('index.html')

def file_checker(filename):
    f = Path((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    if not f.is_file():
        return filename
    else:
        counter = 1
        t = filename
        while f.is_file():
            t = filename
            print("running")
            t = "({}) ".format(str(counter)) + t
            f = Path((os.path.join(app.config['UPLOAD_FOLDER'], t)))
            counter+=1
        return t
    
def print_file(file):
    a = os.path.join(app.config['UPLOAD_FOLDER'], file)
    b = os.path.getatime(a)
    c = os.path.getmtime(a)
    d = os.path.getctime(a)
    e = os.path.getsize(a)
    return b,c,d,e
    

def save_file(filename):
    url = generate_random()
    global name
    con = sqlite3.connect(name)
    cur = con.cursor()
    f = print_file(filename)
    cur.execute("INSERT INTO FILES (ID, NAME, SIZE, TIME) VALUES (?, ?, ?, ?)", (url, filename, f[3], f[0]))
    con.commit()
    cur.close()
    con.close()
    tests(url)
    return url
    
def create_db(name):
    global con
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS FILES (ID, NAME, SIZE, TIME)")
    cur.close()
    con.close()
    con = sqlite3.connect(name)

if __name__ == '__main__':
    create_db(name)
    app.run()
