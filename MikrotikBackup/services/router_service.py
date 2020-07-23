import os,logging,shutil,sys
from distutils.dir_util import copy_tree
from typing import List, Optional

import MikrotikBackup.data.db_session as db_session
from MikrotikBackup.data.router import Router

def get_router_count() -> int:
    session = db_session.create_session()
    session.close()
    return session.query(Router).count()

def get_backup_complete_count() -> int:
    session = db_session.create_session()
    backup_status_query = session.query(Router.backup_status)
    complete_count = 0
    for status in backup_status_query:
        if status == ('Backup Complete',):
            complete_count += 1

    session.close()

    return complete_count

def get_config_complete_count() -> int:
    session = db_session.create_session()
    config_status_query = session.query(Router.config_status)
    complete_count = 0
    for status in config_status_query:
        if status == ('Config Complete',):
            complete_count += 1

    session.close()

    return complete_count

def get_backup_failed_count() -> int:
    session = db_session.create_session()
    backup_status_query = session.query(Router.backup_status)
    failed_count = 0
    for status in backup_status_query:
        if status != ('Backup Complete',):
            failed_count += 1
        if status == ('Backup Skipped',):
            failed_count -= 1

    session.close()

    return failed_count

def get_config_failed_count() -> int:
    session = db_session.create_session()
    config_status_query = session.query(Router.config_status)
    failed_count = 0
    for status in config_status_query:
        if status != ('Config Complete',):
            failed_count += 1
        if status == ('Config Skipped',):
            failed_count -= 1

    session.close()

    return failed_count

def get_unknown_status_count() -> int:
    session = db_session.create_session()
    backup_status_query = session.query(Router.backup_status)
    config_status_query = session.query(Router.config_status)
    unknown_count = 0
    for backup_status in backup_status_query:
        if backup_status == ('Unknown',):
            unknown_count += 1
    for config_status in config_status_query:
        if config_status == ('Unknown',):
            unknown_count += 1

    session.close()

    return unknown_count

def get_router_list() -> List[Router]:
    session = db_session.create_session()
    routers = session.query(Router).\
        order_by(Router.router_name.asc()).\
        all()

    session.close()

    return routers

def get_router_ignore_list() -> List[Router]:
    session = db_session.create_session()
    routers = session.query(Router). \
        filter(Router.ignore == True). \
        all()

    session.close()

    ignored_routers = []
    for r in routers:
        ignored_routers.append(r.router_name)

    return ignored_routers

def get_router_ignore_count() -> int:
    session = db_session.create_session()
    routers = session.query(Router). \
        filter(Router.ignore == True). \
        all()

    session.close()

    ignore_count = 0
    for _ in routers:
        ignore_count += 1

    return ignore_count

def get_router_details(router_name: str)-> Optional[Router]:
    if not router_name:
        return None

    router_name = router_name.strip()

    session = db_session.create_session()

    router = session.query(Router) \
        .filter(Router.router_name == router_name) \
        .first()

    session.close()

    return router

def add_router(router_name,router_ip,username,password,ignore):

    path = os.getcwd()
    print(f'path: {path}')
    directory_exists = os.path.isdir(path + f'/MikrotikBackup/backups/{router_name}')
    print(f"Checking if directory for {router_name} already exists.")

    if directory_exists:
        print("The directory did already exist.")
        return True
    else:
        print("The directory didn't exist.")
        # writes new router to database file
        print("Attempting to write new router to database.")
        r = Router()

        r.router_name = router_name
        r.router_ip = router_ip
        r.username = username
        r.password = password
        r.ignore = ignore

        session = db_session.create_session()
        session.add(r)
        session.commit()
        print("Database entries added successfully.")

        print(f"Attempting to create backup folder for {router_name}")
        try:
            os.mkdir(path + f'/MikrotikBackup/backups/{router_name}')
            f = open(f"router_info/{router_name}.txt", "w+")
            f.write('')
            f.close()
        except:
            print("There was a problem creating backup folder. See the error below.")
            print(sys.exc_info()[1])
        return False

def remove_router(router_name):
    path = os.getcwd()

    print(f"Attempting to remove {router_name} from the database.")
    r = Router()
    session = db_session.create_session()
    router = session.query(Router) \
        .filter(Router.router_name == router_name) \
        .first()
    session.delete(router)
    session.commit()
    print("Router successfully removed from database.")

    print(f"Attempting to remove the backups for {router}.")
    try:
        # Gathering Backups path and removing it
        backup_path = os.path.abspath(os.path.join(os.path.dirname(__file__),f'../backups/{router_name}'))
        shutil.rmtree(backup_path)
        print("Router backups successfully removed.")

        # Gathering Router info.txt path and removing it
        router_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../router_info/{router_name}.txt'))
        os.remove(router_info_path)
        print("Router info successfully removed.")
    except:
        print("There was a problem removing the router's backups. See the error below.")
        print(sys.exc_info()[1])

def update_router(selected_router,router_name, router_ip, username, password, ignore):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../backups/'))

    if router_name != selected_router:
        print(f"Changing name of router from {selected_router} to {router_name}.")
        print(f"Creating new backup directory for {router_name}")

        # creating new backup directory
        try:
            os.mkdir(path + f'/{router_name}')
            print("New backup directory created.")
        except:
            print("There was a problem creating new backup direcotry. See the error below.")
            print(sys.exc_info()[1])

        print("Moving the backups from old direcotry.")

        # moving backup files to new backup directory
        try:
            fromDirectory = path + f'/{selected_router}'
            toDirectory = path + f'/{router_name}'
            copy_tree(fromDirectory, toDirectory)
            print("Files moved successfully.")
        except:
            print("There was a problem moving the backups. See the error below.")
            print(sys.exc_info()[1])

        print("Removing old backups directory.")

        # removing old backup directory
        try:
            shutil.rmtree(path + f'/{selected_router}')
            print("Directory removed successfully.")
        except:
            print("There was a problem removing the directory. See the error below.")
            print(sys.exc_info()[1])

        # # renaming info text file
        # try:
        #     old_info_file =  path + '/{}.txt'.format(selected_router)
        #     new_info_file = path + '/{}.txt'.format(router_name)
        #     os.rename(old_info_file,new_info_file)
        # except:
        #     print("There was a problem renaming the info file. See the error below.")
        #     print(sys.exc_info()[1])

    # updating database values in sql database
    print(f"Updating database values for {selected_router}.")
    session = db_session.create_session()
    r = session.query(Router).filter(Router.router_name == selected_router).one()
    r.router_name = router_name
    r.router_ip = router_ip
    r.username = username
    r.password = password
    r.ignore = ignore
    session.commit()
    print("Database values updated successfully.")

def find_router_by_name(router_name: str) -> Optional[Router]:
    session = db_session.create_session()
    user = session.query(Router).filter(Router.router_name == router_name).first()
    session.close()

    return user
