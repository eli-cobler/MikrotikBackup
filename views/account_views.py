import flask
from flask import request

from infrastructure import cookie_auth
from infrastructure.view_modifiers import response
from services import user_service
from services.user_service import delete_user
from viewmodels.account.index_view_model import IndexViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.register_View_model import RegisterViewModel

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# ################### INDEX #################################
@blueprint.route('/account', methods=['GET'])
@response(template_file='account/index.html')
def index_get():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')

    return vm.to_dict()

@blueprint.route('/account', methods=['POST'])
@response(template_file='account/index.html')
def index_post():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')

    form_id = request.form.get('delete','')
    if form_id == 'delete':
        resp = flask.redirect('/account/logout')
        delete_user(vm.user_id)

        return resp

    return vm.to_dict()

# ################### REGISTER #################################
@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()

    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created.'
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp

# ################### LOGIN #################################
@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    resp = flask.redirect('/router_table')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGOUT #################################
@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp