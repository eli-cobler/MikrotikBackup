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
            print("{} was removed.".format(filename))
            logging.info("%s was removed." % filename)
        except:
            print("There was an issue removeing {}.".format(filename))
            logging.error("There was an issue removing %s." % filename)
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
                    '.DS_Store'] 
    for folder in backup_path:
        if folder in ignore_list:
            print("{} has been ignored.".format(folder))
            logging.info("%s has been ignored." % folder)
        else:
            pass
            print("{} has been checked.".format(folder))
            logging.info("%s has been checked." % folder)
            path = os.path.join(os.getcwd(), 'backups/{}'.format(folder))
            listed = os.listdir(path)
            for file in listed:
                files_date = creation_date(os.path.join(os.getcwd(), 'backups/{}/{}'.format(folder, file)))
                file_path = os.path.join(os.getcwd(), 'backups/{}/{}'.format(folder, file))
                check_date(files_date, file_path)

if __name__ == "__main__":
    run()