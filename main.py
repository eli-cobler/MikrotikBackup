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
import flask
from flask import Flask, render_template, redirect, request, abort, send_file, flash, url_for, Response
import os, add_file, subprocess, time
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
        'ignore_count' : router_service.get_router_ignore_count(),
    }

@app.route('/router_table', methods=['GET', 'POST'])
@response(template_file='home/router_table.html')
def router_table():
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

# takes input form from user to add needed info to the db
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':                    
        router_name = request.form['name']
        router_ip = request.form['router_ip']
        username = request.form['username']
        password = request.form['password']
        if request.form.getlist('skipped') == ['on']:
            ignore = True
        else:
            ignore = False

        exists = router_service.add_router(router_name, router_ip, username, password, ignore)
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

        if request.form.getlist('skipped') == ['on']:
            ignore = True
        else:
            ignore = False

        router_service.update_router(router_to_update,router_name,router_ip,username,password,ignore)
        return redirect(url_for('index'))

    return render_template('home/update.html', routers=routers)

# ################### STREAM SECTION FOR BACKUPS #################################

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route('/run_backup')
def run_backup():
    def backup_background_process():
        top_folder = os.path.dirname(__file__)
        rel_folder = os.path.join('services', 'backup_service.py')
        backup_script_path = os.path.abspath(os.path.join(top_folder, rel_folder))


        proc = subprocess.Popen(
            [f'python3 {backup_script_path}'],
            # call something with a lot of output so we can see it
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline, ''):
            time.sleep(.1)  # Don't need this just shows the text streaming
            yield line.rstrip() + '\n'

    terminal_output = backup_background_process()
    return Response(stream_template('home/stream.html', rows=terminal_output))

@app.route('/single_backup', methods=['GET', 'POST'])
def single_backup():
    routers = router_service.get_router_list()
    
    if request.method == 'POST':
        selected_router = request.form.get('selected router')
        router_details = router_service.get_router_details(selected_router)

        router_ip = router_details.router_ip
        username = router_details.username

        def backup_background_process():
            top_folder = os.path.dirname(__file__)
            rel_folder = os.path.join('services', 'single_backup_service.py')
            backup_script_path = os.path.abspath(os.path.join(top_folder, rel_folder))

            proc = subprocess.Popen(
                [f'python {backup_script_path}'],
                # call something with a lot of output so we can see it
                shell=True,
                universal_newlines=True,
                stdout=subprocess.PIPE
            )

            for line in iter(proc.stdout.readline, ''):
                time.sleep(.1)  # Don't need this just shows the text streaming
                yield line.rstrip() + '\n'

        terminal_output = backup_background_process()
        return Response(stream_template('home/stream.html', rows=terminal_output))

        single_backup_service.run(selected_router,router_ip,username)
        return redirect(url_for('index'))
    
    return render_template('home/single_backup.html', routers=routers)

@app.route('/stream')
def stream():
    def backup_background_process():
        top_folder = os.path.dirname(__file__)
        rel_folder = os.path.join('bin', 'interate.py')
        interate_script_path = os.path.abspath(os.path.join(top_folder, rel_folder))
        proc = subprocess.Popen(
            [f'python {interate_script_path}'],  # call something with a lot of output so we can see it
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline, ''):
            time.sleep(.1)  # Don't need this just shows the text streaming
            yield line.rstrip() + '\n'

    terminal_output = backup_background_process()
    return Response(stream_template('home/stream_progress.html', rows=terminal_output, router_total=router_service.get_router_count()))

# ################### ACCOUNT #################################

# ################### INDEX #################################
@app.route('/account')
@response(template_file='account/index.html')
def register_index():
    return {}
    #render_template('account/index.html')

# ################### REGISTER #################################
@app.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {}

@app.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    r = flask.request

    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        return{
            'name': name,
            'email': email,
            'password': password,
            'error': "Some required fields are missing."
        }

    # TODO: Create user
    # TODO: Log in browser as a session

    return flask.redirect('/account')

# ################### LOGIN #################################
@app.route('/account/login')
def login():
    return render_template('account/login.html')

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