import os
from MikrotikBackup.data import db_session
from MikrotikBackup.services import backup_service, router_details_service

router_name = input("What is the router_name? ")
router_ip = input("What is the router_ip? ")
username = input("What is the username? ")
password = input("What is the password? ")

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('../..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

def run():
    backup_service.create_backup(router_name, router_ip, username)
    backup_service.create_config(router_name, router_ip, username)
    router_details_service.get_info(router_name, router_ip, username)
    router_details_service.parse_info(router_name)

if __name__ == "__main__":
    init_db()
    run()