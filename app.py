from flask import Flask
import os
from data import db_session

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, root_path=dir_path)

def configure():
    register_blueprints()
    setup_db()

def main():
    configure()
    app.run(debug=True, host= '0.0.0.0', port=5006)

def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'mikrotikbackup.sqlite')

    db_session.global_init(db_file)

def register_blueprints():
    from views import home_views
    from views import account_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)

if __name__ == '__main__':
    main()
