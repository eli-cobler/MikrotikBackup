#
#  main.py
#  MikrotikBackup
#
#  Created by Eli Cobler on 11/18/18.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router backup.
#
#  Runs the mian flask app.

from flask import Flask, render_template, redirect, request
import updateDB

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':                    
        name = request.form['name']
        router_ip = request.form['router_ip']
        username = request.form['username']
        password = request.form['password']

        updateDB.add(name, router_ip, username, password)

    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    return render_template('remove.html')

app.run(debug=True, host='0.0.0.0')