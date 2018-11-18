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
import database

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

        database.add(name, router_ip, username, password)

    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    router_list = database.read()
    routers = []
    for item in router_list:
        data = item.split(':')
        routers.append(data[0])

    if request.method == 'POST':
        router_to_remove = request.form.get('selected router')
        database.remove(router_to_remove)

    
    return render_template('remove.html', routers=routers)

app.run(host='0.0.0.0')