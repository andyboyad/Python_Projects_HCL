#Assignment 4
#Author: Andrew Boyadjiev
#Technologies: flask, sqlite3, werkzeug
#Description:   Flask server downloads and uploads files from user
#               User can access the file via unique ID of length 30
#               Users can upload, download, or delete files
#               Links to files is stored in a sqlite database
#Note: Make sure to specify the upload directory in upload_dir.txt
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

#Generates random ID link for file of length 30
def generate_random():
    l = [chr(randint(97,122)) for i in range(30)]
    return "".join(l)

#Deletes File and ID to file from sqlite database
def delete_id(ID):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur = cur.execute("SELECT * FROM FILES WHERE ID=?", (ID,))
    data = cur.fetchall()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data[0][1]))
    cur.execute("DELETE FROM FILES WHERE ID=?", (ID,))
    con.commit()
    cur.close()
    con.close()

#Gets the file name from ID for downloading
def download_from_id(ID):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("SELECT * FROM FILES WHERE ID=?", (ID,))
    data = cur.fetchall()
    cur.close()
    con.close()
    if not data:
        return []
    return data[0]

#Route for downloading the file
@app.route('/file/<ID>')
def get_file(ID):
    d = download_from_id(ID)
    print(d)
    if not d:
        return "File not found"
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], d[1]), as_attachment=True)

#Route for the download page of the file
@app.route('/download/<ID>')
def download(ID):
    d = download_from_id(ID)
    print(d)
    if not d:
        return "File not found"
    return render_template("download.html", ID=d[0], name=d[1], size=d[2], size2 = round(d[2]/1000), size3 = round(d[2]/1000000))

#Route for deleting the file based on ID
@app.route('/delete/<ID>')
def delete(ID):
    d = download_from_id(ID)
    if not d:
        return "File does not exist"
    delete_id(ID)
    return render_template("delete.html", name=d[1])

#Handles when user uploads a file to the server through request
@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
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
        filename = file_checker(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        g = save_file(filename)
        return render_template('success.html', ID=g)
    return render_template('index.html')

#Landing page of the file service
@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

#Changes the name of the file if theres a duplicate on the server
def file_checker(filename):
    f = Path((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    if not f.is_file():
        return filename
    else:
        counter = 1
        t = filename
        while f.is_file():
            t = filename
            t = "({}) ".format(str(counter)) + t
            f = Path((os.path.join(app.config['UPLOAD_FOLDER'], t)))
            counter+=1
        return t

#For getting the details of the file
def print_file(file):
    a = os.path.join(app.config['UPLOAD_FOLDER'], file)
    b = os.path.getatime(a)
    c = os.path.getmtime(a)
    d = os.path.getctime(a)
    e = os.path.getsize(a)
    return b,c,d,e
    
#Saves file name and its ID link into the database
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
    return url

#Creates the database
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
    #app.run(ssl_context='adhoc')
    app.run()
