import os, flask
from flask import request, redirect, url_for, render_template, abort, send_file
from MikrotikBackup import add_file
from MikrotikBackup.data import db_session
from MikrotikBackup.infrastructure import cookie_auth
from MikrotikBackup.infrastructure.view_modifiers import response
from MikrotikBackup.services import router_service
from MikrotikBackup.viewmodels.home.add_view_model import AddViewModel
from MikrotikBackup.viewmodels.home.index_view_model import IndexViewModel
from MikrotikBackup.viewmodels.home.remove_view_model import RemoveViewModel
from MikrotikBackup.viewmodels.home.router_info_view_model import RouterInfoViewModel
from MikrotikBackup.viewmodels.home.update_view_model import UpdateViewModel

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

# ################### Database Setup #################################
def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'mikrotikbackup.sqlite')

    db_session.global_init(db_file)


# ################### Return Files for viewing and downloading files #################################
@blueprint.route('/', defaults={'req_path': ''})
@blueprint.route('/<path:req_path>')
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


@blueprint.route('/', methods=['GET', 'POST'])
@response(template_file='home/index.html')
def index():
    vm = IndexViewModel()

    resp = flask.redirect('/account/login')
    cookie_auth.set_auth(resp, vm.user_id)

    return resp


@blueprint.route('/router_table', methods=['GET'])
@response(template_file='home/router_table.html')
def router_table():
    vm = IndexViewModel()

    return vm.to_dict()


@blueprint.route('/router-info/<router_name>')
@response(template_file='home/details.html')
def router_info(router_name: str):
    vm = RouterInfoViewModel()

    if not vm.router_name:
        return flask.abort(status=404)

    if not vm.router:
        return flask.abort(status=404)

    return vm.to_dict()


# takes input form from user to add needed info to the db
@blueprint.route('/add', methods=['GET'])
@response(template_file='home/add.html')
def add_get():
    vm = AddViewModel()
    return vm.to_dict()


@blueprint.route('/add', methods=['POST'])
@response(template_file='home/add.html')
def add_post():
    vm = AddViewModel()

    vm.validate()

    if vm.error:
        return vm.to_dict()

    if request.form.getlist('skipped') == ['on']:
        ignore = True
    else:
        ignore = False

    exists = router_service.add_router(vm.router_name, vm.router_ip, vm.username, vm.password, ignore)
    add_file.autoUpdater(vm.router_name, vm.router_ip, vm.username, vm.password)
    add_file.ssh_key(vm.username, vm.password, vm.router_ip)

    if exists:
        vm.error = "This has already be Added or the folder already exists in backups directory."
        return vm.to_dict()

    resp = flask.redirect('/router_table')
    cookie_auth.set_auth(resp, vm.user_id)

    return resp


# allows user to select which location to remove viva dropdown menu
@blueprint.route('/remove', methods=['GET'])
@response(template_file='home/remove.html')
def remove_get():
    vm = RemoveViewModel()
    return vm.to_dict()

@blueprint.route('/remove', methods=['POST'])
@response(template_file='home/remove.html')
def remove_post():
    vm = RemoveViewModel()

    router_service.remove_router(vm.router_to_remove)

    resp = flask.redirect('/router_table')
    cookie_auth.set_auth(resp, vm.user_id)

    return resp


# allows users to update already existing routers in the database file
@blueprint.route('/update', methods=['GET'])
@response(template_file='home/update.html')
def update_get():
    vm = UpdateViewModel()
    return vm.to_dict()

@blueprint.route('/update', methods=['POST'])
@response(template_file='home/update.html')
def update_post():
    vm = UpdateViewModel()

    router_details = router_service.get_router_details(vm.router_to_update)

    if vm.router_name == '':
        router_name = vm.router_to_update
    else:
        router_name = vm.router_name

    if vm.router_ip == '':
        router_ip = router_details.router_ip
    else:
        router_ip = vm.router_ip

    if vm.username == '':
        username = router_details.username
    else:
        username = vm.username

    if vm.password == '':
        password = router_details.password
    else:
        password = vm.password

    if request.form.getlist('skipped') == ['on']:
        ignore = True
    else:
        ignore = False

    router_service.update_router(vm.router_to_update, router_name, router_ip, username, password, ignore)

    resp = flask.redirect('/router_table')
    cookie_auth.set_auth(resp, vm.user_id)

    return resp


# ################### STREAM SECTION FOR BACKUPS #################################
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@blueprint.route('/run_backup')
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


@blueprint.route('/single_backup', methods=['GET', 'POST'])
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

        single_backup_service.run(selected_router, router_ip, username)
        return redirect(url_for('index'))

    return render_template('home/single_backup.html', routers=routers)


@blueprint.route('/stream')
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
    return Response(stream_template('home/stream_progress.html', rows=terminal_output,
                                    router_total=router_service.get_router_count()))