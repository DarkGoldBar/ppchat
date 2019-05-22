#! /usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import random

import flask
from flask import Flask, session, redirect, url_for, escape, request, render_template

from .idgen import gen_once 
from .models import myUser, myMessage

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        flask.flash(random.choice(["wow", "yeah", "nice", "right", "ouch", "ohh"]))
        return redirect(url_for('index'))
    return render_template('bs-base.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        user = myUser(username)
        if user.authorize(password):
            session["username"] = username
        return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('index'))

@app.route('/idgen', methods=['GET', 'POST'])
def idgen():
    if request.method == 'POST':
        region_code = request.form.get('inputRegion')
        region_code = int(region_code) if region_code else None
        date_code = request.form.get('inputDate')
        date_code = int(date_code) if date_code else None
        data = {
            'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            'idnum': gen_once(region_code, date_code),
            'comment': "No comment"
        }
        idgen_history = session.get("idgen_history")
        if not idgen_history:
            idgen_history = [data]
        else:
            idgen_history.insert(0, data)
        if len(idgen_history) > 10:
            idgen_history.pop(-1)
        session["idgen_history"] = idgen_history
        return redirect("idgen")
    else:
        return render_template('idgen.html', idgen_history = session.get("idgen_history", []))

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if 'username' not in session:
        return render_template('error.html', message="登陆后才能聊天")
    if request.method == 'POST':
        to = request.form.get('to')
        message = request.form.get('message')
        msg = myMessage(session['username'], to, message)
    messages = []
    messages.append(myMessage(session['username'], "system", "Hello, system"))
    messages.append(myMessage("system", session['username'], "Hello, user"))
    html = render_template('chatroom.html', messages=messages)
    return html

# @app.errorhandler(500)
# def page_error(e):
#     return render_template('error.html'), 500

# @app.errorhandler(404)
# def page_error(e):
#     return render_template('error.html', message="404 not found"), 404

# set the secret key.  keep this really secret:
app.secret_key = b'b\xd1\x10#\xe3\xca\xfd\\A\x10\xffh\xff\xbc\x92\x10<\x92\x11G[*\xa5['
app.permanent_session_lifetime = 3600*24*7

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=6778)