#!/usr/local/bin/python
# coding=utf-8
import os
from flask import Flask, render_template, jsonify,request, session, redirect, url_for
import json, random
import subprocess
import uuid
import os
import sqlite3
import requests
import grequests
import urllib
import locale
from requests_futures.sessions import FuturesSession
# from flask.ext.mysql import MySQL
# import MySQLdb as mdb

app = Flask(__name__)
locale.setlocale(locale.LC_ALL, 'en_US')

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
    # requests.get("http://localhost:8080/fetch_comments", params={'url': 'http%3A%2F%2Fwww.regulations.gov%2Fexportdocket%3FdocketId%3DICEB-2015-0002'})
    if 'username' not in session:
        return redirect(url_for('login'))
    cursor, db = get_cursor()
    q = "SELECT id, tag, link, status, total_count FROM active_analysis WHERE uid = ?"
    cursor.execute(q, (session['uid'],))
    rows = cursor.fetchall()
    obj_arr = []
    comments_processed = 0
    for row in rows:
        obj = {}
        obj['id'] = row['id']
        obj['tag'] = row['tag']
        obj['link'] = row['link']
        obj['status'] = row['status']
        obj['count'] = locale.format("%d", row['total_count'], grouping=True)
        if row['total_count'] == 0 :
            resp = int(requests.get('http://localhost:8080/get_count?token=' + str(row['id'])).text)
            if resp:
                obj['count'] = locale.format("%d", resp, grouping=True)
            else:
                resp = 0
            total_comments += resp
        obj_arr.append(obj)
        if row['id'] == 1:
            comments_processed = obj['count']
            total_comments = row['total_count']
    # q = "SELECT count(id) cnt FROM active_analysis WHERE status != 1"
    # cursor.execute(q)
    # row = cursor.fetchone()
    # resp = 0
    # totc = 0
    # if not row:
        # active_count = 0
    # else:
    #     resp = int(requests.get('http://localhost:8080/get_count?token=' + str(row['id'])).text)
    #     if resp:
    #         active_count = int(resp)
    #     else:
    #         resp = int(0)
    #     # TODO uncomment this
    #     # resp = 0
    #     total_comments += resp
	# totc = resp


    total_comments = locale.format("%d", total_comments, grouping=True)
    return render_template('index.html', analysis=obj_arr, acount=active_count, totc=0, cprocessed = comments_processed, cfetched=total_comments)

@app.route('/start-analysis', methods=['GET', 'POST', 'REQUEST'])
def startAnalysis():
    if 'uid' not in session:
        return redirect(url_for('login'))
    if not request.form:
        return redirect(url_for('indexMain'))
    cursor, db = get_cursor()
    docketlink = request.form['docketlink']
    dockettag = request.form['dockettag']
    q = "INSERT INTO active_analysis (uid, link, tag, status) VALUES (?, ?, ?, 0)"
    cursor.execute(q, (session['uid'], docketlink, dockettag,))
    db.commit()
    url = urllib.urlencode({'url': docketlink})
    session_f = FuturesSession()
    future_one = session_f.get('http://localhost:8080/fetch_comments?' + url + '&token=' + str(cursor.lastrowid))
    # urls = ['http://localhost:8080/fetch_comments?' + url]
    # rs = (grequests.get(u) for u in urls)
    # grequests.map(rs)
    return redirect(url_for('indexMain'))

@app.route('/detailed_analysis', methods=['GET', 'POST', 'REQUEST'])
def detailedAnalysis():
    if 'uid' not in session:
        return redirect(url_for('login'))
    # if not request.form:
        # return redirect(url_for('indexMain'))
    cursor, db = get_cursor()
    if request.args.get('id'):
        analysis_id = int(request.args.get('id'))
    q = "SELECT total_count, tag from active_analysis WHERE id = ?"
    cursor.execute(q, (analysis_id,))
    row = cursor.fetchone()
    tag = row['tag']
    if analysis_id == 1:
        cfetched = locale.format("%d", row['total_count'], grouping=True)
        return render_template('detailed-analysis-1.html', cfetched=cfetched, tag=tag)

    cfetched = 0
    comments = ''
    ## TODO uncomment
    resp = int(requests.get('http://localhost:8080/get_count?token=' + str(analysis_id)).text)
    # resp = 0
    if resp:
        cfetched += int(resp)


    ## TODO uncomment
    resp = requests.get('http://localhost:8080/get_top?token=' + str(analysis_id)).text
    resp = resp.split('~~')
    ## TODO comment
    # resp = "this is a new tag ~~ this is fine ~~ that is fine ~~".split('~~')
    obj_arr = []
    if resp:
        comments = resp
        for comment in comments:
            obj = {}
            obj['heading'] = comment[:100]
            if len(comment) > 100:
                 obj['heading'] += '...'
            obj['content'] = comment
            obj_arr.append(obj)

    comments = obj_arr
    base_path = os.path.dirname(os.path.abspath(__file__))
    graphnames = ['1' , '2-0', '2-1', '3']
    valid_graphs = []
    for graph in graphnames:
        graph_path = base_path + graph + str(analysis_id)
        if os.path.isfile(graph_path + '.png'):
            valid_graphs.append(graph)

    return render_template('detailed-analysis.html', cfetched=cfetched, comments=comments, tag=tag, valid_graphs=valid_graphs, analysis_id=analysis_id)



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

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('uid', None)
    return redirect(url_for('indexMain'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98MMosfggkaniaa-191emp01925PKOida81IANL1!!##~245!jmN]LWX/,?RT'

if __name__ == "__main__":
    # app.run(threaded=True)
    app.run(debug=True, threaded=True, host='::')
