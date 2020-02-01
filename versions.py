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

# log setup
logging.basicConfig(filename='logs/versions.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def filename_date(filename):
    date = os.path.basename(filename).split('_')[0]
    return date

def creation_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def check_date(filename, file_path):
    compare_date = datetime.now() - timedelta(days=21)

    if filename < compare_date:
        try:
            os.remove(str(file_path))
            print(f"{filename} was removed.")
            logging.info(f"{filename} was removed.")
        except:
            print(f"There was an issue removeing {filename}.")
            logging.error(f"There was an issue removing {filename}.")
            logging.error(sys.exc_info()[1])
    else: 
        pass

def run():
    backup_path = os.listdir(os.path.join(os.getcwd(), 'backups'))
    ignore_list = ['Broadway Liquor',
                    'Spectrum Voice',
                    'CASA',
                    'Value Med Midwest City',
                    'Valu Med Harrah',
                    'Value Med FTG',
                    'GPSS Hobart',
                    '.DS_Store',
                    'SPARK Datacenter',
                   'GPSS-CNH - EOMC - Poteau',
                   'Pinedale']
    for folder in backup_path:
        if folder in ignore_list:
            print(f"{folder} has been ignored.")
            logging.info(f"{folder} has been ignored.")
        else:
            pass
            print(f"{folder} has been checked.")
            logging.info(f"{folder} has been checked.")
            path = os.path.join(os.getcwd(), f'backups/{folder}')
            listed = os.listdir(path)
            for file in listed:
                files_date = creation_date(os.path.join(os.getcwd(), f'backups/{folder}/{file}'))
                file_path = os.path.join(os.getcwd(), f'backups/{folder}/{file}')
                check_date(files_date, file_path)

if __name__ == "__main__":
    run()