#
#  versions.py
#  MikrotikBakcup
#
#  Created by Eli Cobler on 01/27/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  This file allows you to keep only 21 days worth of backups. 

import os
from datetime import datetime, timedelta

def filename_date(filename):
    date = os.path.basename(filename).split('_')[0]
    return date

def creation_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def check_date(filename, file_path):
    compare_date = datetime.now() - timedelta(days=21)
    print(filename)
    print(compare_date)

    if filename < compare_date:
        print("True")
        os.remove(str(file_path))
    else: 
        print("False")
        pass

def run():
    backup_path = os.listdir(os.path.join(os.getcwd(), 'backups')) 
    for folder in backup_path:
        if folder == '.DS_Store':
            pass
        else:
            print(folder)
            path = os.path.join(os.getcwd(), 'backups/{}'.format(folder))
            print(path)
            listed = os.listdir(path)
            for file in listed:
                files_date = creation_date(os.path.join(os.getcwd(), 'backups/{}/{}'.format(folder, file)))
                file_path = os.path.join(os.getcwd(), 'backups/{}/{}'.format(folder, file))
                print(file_path)
                check_date(files_date, file_path)

if __name__ == "__main__":
    run()