#!/usr/local/bin/python
# coding=utf-8
import os
from flask import Flask, render_template, jsonify,request, session, redirect, url_for
import json, random
import subprocess
import uuid
import os
import sqlite3
import request
# from flask.ext.mysql import MySQL
# import MySQLdb as mdb

app = Flask(__name__)

def get_cursor():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(base_dir + "/appdb.db")
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    return conn.cursor(), conn


# mysql = MySQL()

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'crowdsource'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'crowdsource'
# app.config['MYSQL_DATABASE_DB'] = 'crowdsource_connectivity'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# conn =  mdb.connect('localhost', 'crowdsource', 'crowdsource', 'crowdsource_connectivity');
# conn = mysql.connect()

# cursor = conn.cursor(mdb.cursors.DictCursor)

@app.route('/static/<name>')
def sendFile(fileName = None):
    return send_from_directory('static', fileName)

@app.route('/index.html')
@app.route('/', methods=['GET', 'POST', 'REQUEST'])
def indexMain():
    requests.get("http://localhost:8080/fetch_comments", params={'url': 'http%3A%2F%2Fwww.regulations.gov%2Fexportdocket%3FdocketId%3DICEB-2015-0002'}
)
    if 'username' not in session:
        return redirect(url_for('login'))
    cursor, db = get_cursor()
    q = "SELECT id, tag, link, status FROM active_analysis WHERE uid = ?"
    print session
    cursor.execute(q, (session['uid'],))
    rows = cursor.fetchall()
    obj_arr = []
    for row in rows:
        obj = {}
        obj['id'] = row['id']
        obj['tag'] = row['tag']
        obj['link'] = row['link']
        obj['status'] = row['status']
        obj_arr.append(obj)
    print obj_arr
    return render_template('index.html', analysis=obj_arr)

@app.route('/start-analysis', methods=['GET', 'POST', 'REQUEST'])
def startAnalysis():
    if 'uid' not in session:
        return redirect(url_for('login'))
    if not request.form:
        return redirect(url_for('indexMain'))
    cursor, db = get_cursor()
    docketlink = request.form['docketlink']
    dockettag = request.form['dockettag']
    q = "INSERT INTO active_analysis (uid, link, tag) VALUES (?, ?, ?)"
    print cursor
    cursor.execute(q, (session['uid'], docketlink, dockettag,))
    db.commit()
    return redirect(url_for('indexMain'))

@app.route('/detailed_analysis', methods=['GET', 'POST', 'REQUEST'])
def detailedAnalysis():
    if 'uid' not in session:
        return redirect(url_for('login'))
    # if not request.form:
        # return redirect(url_for('indexMain'))
    cursor, db = get_cursor()
    # docketlink = request.form['docketlink']
    # dockettag = request.form['dockettag']
    # q = "INSERT INTO active_analysis (uid, link, tag) VALUES (?, ?, ?)"
    # print cursor
    # cursor.execute(q, (session['uid'], docketlink, dockettag,))
    # db.commit()
    return render_template('detailed-analysis.html')



@app.route('/login', methods=['GET', 'POST', 'REQUEST'])
def login():
    if 'username' in session:
        return redirect(url_for('indexMain'))
    if not request.form:
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    cursor, db = get_cursor()
    q = "SELECT id, username FROM user WHERE username = ? and password = ?"
    cursor.execute(q, (username, password,))
    row = cursor.fetchone()
    if not row:
        return render_template('login.html')
    else:
        session['username'] = row['username']
        session['uid'] = row['id']
        return redirect(url_for('indexMain'))

    return render_template('login.html')

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98MMosfggkaniaa-191emp01925PKOida81IANL1!!##~245!jmN]LWX/,?RT'

if __name__ == "__main__":
    # app.run(threaded=True)
    app.run(debug=True, threaded=True, host='::')
