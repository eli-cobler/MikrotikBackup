#
#   removeBackupFiles.py
#   MikrotikBakcup
#
#   Created by Eli Cobler on 06/13/19.
#   Copyright © 2018 Eli Cobler. All rights reserved.
#
#   This project allows you generate and store backup and config
#  files from Mikrotik Routers.
#
#   This file removes all backup files from the router keeping them from filling up on backups.

# python module imports
import os,sys, subprocess
from datetime import datetime
from tqdm import tqdm

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

# project module imports
import data.db_session as db_session
from services import router_service

# log setup
log_date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


def run():
    tqdm.write(f"{log_date_time} Gathering Routers...")
    print(f"{log_date_time} Gathering Routers...")

    ignore_list = router_service.get_router_ignore_list()
    router_list = router_service.get_router_list()
    router_count = router_service.get_router_count()

    tqdm.write(f"{log_date_time} Routers Gathered.")
    print(f"{log_date_time} Routers Gathered.")

    for item in tqdm(router_list, total=router_count, unit=" routers"):
        tqdm.write(f"{log_date_time} Starting Removal for {item.router_name}...")
        print(f"{log_date_time} Starting Removal for {item.router_name}...")

        if item.router_name in ignore_list:
            tqdm.write(f"{log_date_time} Removal skipped.")
            print(f"{log_date_time} Removal skipped.")
        else:
            try:
                remove_backup = subprocess.run(f'ssh {item.username}@{item.router_ip} /file remove [find type="backup"]',
                                               shell=True,
                                               universal_newlines=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                if remove_backup.stdout != '':
                    print(f"{log_date_time} {remove_backup.stdout}")
                    tqdm.write(f"{log_date_time} stdout: {remove_backup.stdout}")

                if remove_backup.stderr != '':
                    print(f"{log_date_time} {remove_backup.stderr}")
                    tqdm.write(f"{log_date_time} stderr: {remove_backup.stderr}")
            except:
                print(f'{log_date_time} {sys.exc_info()[1]}')
                tqdm.write(f"{log_date_time} Exception: {sys.exc_info()[1]}")

            tqdm.write(f"{log_date_time} Removal for {item.router_name} completed.")
            print(f"{log_date_time} Removal for {item.router_name} completed.")



if __name__ == "__main__":
    init_db()
    run()