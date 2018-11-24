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
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        routers.append(data[0])

    if request.method == 'POST':
        router_to_remove = request.form.get('selected router')
        database.remove(router_to_remove)

    
    return render_template('remove.html', routers=routers)

@app.route('/update', methods=['GET', 'POST'])
def update():
    router_list = database.get()
    routers_list = []
    for item in router_list:
        data = item.split(':')
        routers_list.append(data[0])

    routers_dict = {}
    for item in router_list:
        data = item.split(':')
        routers_dict[data[0]] = [data[1], data[3], data[4]]

    if request.method == 'POST':
        router_to_update = request.form.get('selected router')

        if request.form['name'] == '':
            name = router_to_update
        else:
            name = request.form['name']
        
        if request.form['router_ip'] == '':
            router_ip_list = routers_dict.get(router_to_update)
            router_ip = router_ip_list[0]
        else:
            router_ip = request.form['router_ip']

        if request.form['username'] == '':
            username_list = routers_dict.get(router_to_update)
            username = username_list[1]
        else:
            username = request.form['username']

        if request.form['password'] == '':
            password_list = routers_dict.get(router_to_update)
            password = password_list[2]
        else:
            password = request.form['password']

        database.update(name, router_ip, username, password, router_to_update)

    return render_template('update.html', routers=routers_list)

@app.route('/success')
def success():
    render_template('success.html')

app.run(host='0.0.0.0')