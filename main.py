#
#  main.py
#  MikrotikBackup
#
#  Created by Eli Cobler on 11/18/18.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  Runs the main flask app.
import time

import flask
from flask import Flask, render_template, redirect, request, abort, send_file, flash, url_for
import database, backup, os, add_file
import data.db_session as db_session
from infrastructure.view_modifiers import response
from services import router_service, single_backup_service, backup_service

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/', methods=['GET', 'POST'])
@response(template_file='home/index.html')
def index():
    return {
        'routers':router_service.get_router_list(),
        'router_count': router_service.get_router_count(),
        'backup_complete_count': router_service.get_backup_complete_count(),
        'config_complete_count': router_service.get_config_complete_count(),
        'backup_failed_count': router_service.get_backup_failed_count(),
        'config_failed_count': router_service.get_config_failed_count(),
        'unknown_count': router_service.get_unknown_status_count(),
    }

@app.route('/router-info/<router_name>')
@response(template_file='home/details.html')
def router_info(router_name: str):
    if not router_name:
        return flask.abort(status=404)

    router = router_service.get_router_details(router_name.strip())
    if not router:
        return flask.abort(status=404)

    uptime = '0hrs'
    version = '0.0.0'
    free_memory = '0.0MiB'
    total_memory = '0.0Mib'
    cpu_load = '0%'
    free_hdd_space = '0.0MiB'
    total_hdd_space = '0.0MiB'
    bad_blocks = "0%"
    board_name = 'Mikrotik'

    if router:
        uptime = router.uptime
        version = router.router_os_version
        free_memory = router.free_memory
        total_memory = router.total_memory
        cpu_load = router.cpu_load
        free_hdd_space = router.free_hdd_space
        total_hdd_space = router.total_hdd_space
        bad_blocks = router.bad_blocks
        board_name = router.board_name

    return {
        'router_name': router_name,
        'uptime': uptime,
        'version': version,
        'free_memory': free_memory,
        'total_memory': total_memory,
        'cpu_load': cpu_load,
        'free_hdd_space': free_hdd_space,
        'total_hdd_space': total_hdd_space,
        'bad_blocks': bad_blocks,
        'board_name': board_name,
    }

# takes input form from user to add needed info to the database file
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':                    
        router_name = request.form['name']
        router_ip = request.form['router_ip']
        username = request.form['username']
        password = request.form['password']

        exists = router_service.add_router(router_name, router_ip, username, password)
        add_file.autoUpdater(router_name, router_ip, username, password)
        add_file.ssh_key(username, password, router_ip)

        if exists:
            flash("This has already be Added or the folder already exists in backups directory.")
        else:
            return redirect(url_for('index'))

    return render_template('home/add.html')

# allows user to select which location to remove viva dropdown menu
@app.route('/remove', methods=['GET', 'POST'])
def remove():
    routers = router_service.get_router_list()
    if request.method == 'POST':
        router_to_remove = request.form.get('selected router')
        router_service.remove_router(router_to_remove)
        return redirect(url_for('index'))
    
    return render_template('home/remove.html', routers=routers)

# allows users to update already existing routers in the database file
@app.route('/update', methods=['GET', 'POST'])
def update():
    routers = router_service.get_router_list()

    if request.method == 'POST':
        router_to_update = request.form.get('selected router')
        router_details = router_service.get_router_details(router_to_update)

        if request.form['name'] == '':
            router_name = router_to_update
        else:
            router_name = request.form['name']
        
        if request.form['router_ip'] == '':
            router_ip = router_details.router_ip
        else:
            router_ip = request.form['router_ip']

        if request.form['username'] == '':
            username = router_details.username
        else:
            username = request.form['username']

        if request.form['password'] == '':
            password = router_details.password
        else:
            password = request.form['password']

        router_service.update_router(router_to_update,router_name,router_ip,username,password)
        return redirect(url_for('index'))

    return render_template('home/update.html', routers=routers)

@app.route('/run_backup', methods=['GET', 'POST'])
@response(template_file='home/run_backup.html')
def run_backup():
    routers = router_service.get_router_list()

    # if request.method == 'GET':
    #     backup_service.run()

    return {
        'routers': routers,
        'router_total': router_service.get_router_count(),
    }

@app.route('/single_backup', methods=['GET', 'POST'])
def single_backup():
    routers = router_service.get_router_list()
    
    if request.method == 'POST':
        selected_router = request.form.get('selected router')
        router_details = router_service.get_router_details(selected_router)

        router_ip = router_details.router_ip
        username = router_details.username

        single_backup_service.run(selected_router,router_ip,username)
        return redirect(url_for('index'))
    
    return render_template('home/single_backup.html', routers=routers)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = os.getcwd()

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    backup_folder = os.path.basename(req_path)

    # Show directory contents
    files = os.listdir(abs_path)
    files.sort(reverse=True)
    return render_template('home/files.html', files=files, backups=backup_folder)

def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'mikrotikbackup.sqlite')

    db_session.global_init(db_file)

setup_db()
app.run(debug=True, host='0.0.0.0')