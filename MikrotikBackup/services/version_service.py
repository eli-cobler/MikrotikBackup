#
#  version_service.py
#  MikrotikBakcup
#
#  Created by Eli Cobler on 01/27/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  This file allows you to keep only 21 days worth of backups.

import os,logging,sys
from datetime import datetime,timedelta
from tqdm import tqdm

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)

# project module imports
import MikrotikBackup.data.db_session as db_session
from MikrotikBackup.services import router_service

# log setup
log_date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

def main():
    init_db()
    run()

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

def filename_date(filename):
    return os.path.basename(filename).split('_')[0]

def creation_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def check_date(filename, file_path):
    compare_date = datetime.now() - timedelta(days=21)

    if filename < compare_date:
        try:
            os.remove(str(file_path))
            tqdm.write(f"{filename} was removed.")
            print(f'{log_date_time} {filename} was removed.')
        except:
            tqdm.write(f"There was an issue removeing {filename}.")
            print(f'{log_date_time} There was an issue removing {filename}.')
            print(f'{log_date_time} {sys.exc_info()[1]}')

def run():
    top_folder = os.path.dirname(__file__)
    rel_folder = os.path.join('..', 'backups')
    backups_path = os.path.abspath(os.path.join(top_folder, rel_folder))
    backups_path_listdir = os.listdir(backups_path)

    ignore_list = router_service.get_router_ignore_list()
    for folder in tqdm(backups_path_listdir, unit=" files"):
        if folder in ignore_list:
            tqdm.write(f"{folder} has been ignored.")
            print(f'{log_date_time} {folder} has been ignored.')
        elif folder =='.DS_Store':
            tqdm.write(f'Found .ds_store in {folder}')
        elif folder =='PlaceHolder.txt':
            tqdm.write(f'Found the placeholder.txt')
        else:
            tqdm.write(f"{folder} is being checked.")
            print(f'{log_date_time} {folder} has been checked.')
            path = os.path.join(backups_path, folder)
            listed = os.listdir(path)
            for file in listed:
                files_date = creation_date(os.path.join(backups_path, folder, file))
                file_path = os.path.join(backups_path, folder, file)
                check_date(files_date, file_path)

            tqdm.write(f"{folder} has been checked.")
            print(f'{log_date_time} {folder} has been checked.')

if __name__ == "__main__":
    main()