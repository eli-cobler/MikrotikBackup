#
#  database.py
#  MikrotikBackup
#
#
#  Created by Eli Cobler on 01/27/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you generate and store backup and config
#  files from Mikrotik Routers.
#
#  This file allows you to add, update, &, remove routers to the Oxidized db file.

import os,shutil,logging,sys
from distutils.dir_util import copy_tree

# paths to database file one for testing local, other for remote server
filepath = os.getcwd() + 'mikrotik_backup/resources/router.db'

# log setup
logging.basicConfig(filename='logs/database.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

def get():      
    router_list = []
    # Appends all lines of the file to a list for removal later
    with open(filepath, 'r+') as database:
        for line in database:
            router_list.append(line)
    database.close()

    return router_list

def add(name, router_ip, username, password):
    path = os.getcwd()
    directory_exists = os.path.isdir(path + '/backups/{}'.format(name))
    logging.info("Checking if directory for %s already exists." % name)
    
    if directory_exists:
        logging.info("The directory did already exist.")
        return True
    else:
        logging.info("The directory didn't exist.")
        # writes new router to database file
        logging.info("Attempting to write new router to database.")
        try:
            with open(filepath, 'a') as f:
                f.write("{}:{}:{}:{}:Not Set:Not Set:Not Set:Not Set\n".format(name,router_ip,username,password))
            logging.info("Database entry added successfully.")
        except:
            logging.error("There was a problem writing to the database. See the error below.")
            logging.error(sys.exc_info()[1])
        
        logging.info("Attempting to create backup folder for %s" % name)
        try:
            os.mkdir(path + '/backups/{}'.format(name))
            f = open("router_info/{}.txt".format(name), "w+")
            f.write('')
            f.close
        except:
            logging.error("There was a problem creating backup folder. See the error below.")
            logging.error(sys.exc_info()[1])
        return False

# This function completely removes a router, including the backup files. 
def complete_removal(router):
    router_list = get()
    path = os.getcwd()

    logging.info("Attempting to remove %s from the database." % router)
    try:
        with open(filepath, 'w') as output:
            for item in router_list:
                if router not in item:
                    output.write(item)
        output.close()
        logging.info("Router successfully removed from database.")
    except:
        logging.error("There was a problem removing the router from the database. See the error below.")
        logging.error(sys.exc_info()[1])
    
    logging.info("Attempting to remove the backups for %s." % router)
    try:
        shutil.rmtree(path + '/backups/{}'.format(router))
        logging.info("Router backups successfully removed.")
        os.remove('router_info/{}.txt'.format(router))
    except:
        logging.error("There was a problem removing the router's backups. See the error below.")
        logging.error(sys.exc_info()[1])

# This function reads each line in the database file then removes the unwanted router.
# Used in update function.
def remove(router):
    router_list = get()
        
    with open(filepath, 'w') as output:
        for item in router_list:
            if router not in item:
                output.write(item)
    output.close()

# Uses remove function to rewrite the whole database file removing old 
# router info and replacing it with updated info
def update(name, router_ip, username, password, selected_router, backup_status, config_status, backup_date, version):
    path = os.getcwd()
    
    if name != selected_router:
        logging.info("Changing name of router from %s to %s." % (selected_router,name))
        logging.info("Creating new backup directory for %s" % name)
        try:
            os.mkdir(path + '/backups/{}'.format(name))
            logging.info("New backup directory created.")
        except:
            logging.error("There was a problem creating new backup direcotry. See the error below.")
            logging.error(sys.exc_info()[1])

        logging.info("Moving the backups from old direcotry.")
        try:
            fromDirectory = path + '/backups/{}'.format(selected_router)
            toDirectory = path + '/backups/{}'.format(name)
            copy_tree(fromDirectory, toDirectory)
            logging.info("Files moved successfully.")
        except:
            logging.error("There was a problem moving the backups. See the error below.")
            logging.error(sys.exc_info()[1])

        logging.info("Removing old backups directory.")
        try:
            shutil.rmtree(path + '/backups/{}'.format(selected_router))
            logging.info("Directory removed successfully.")
        except:
            logging.error("There was a problem removing the direcotry. See the error below.")
            logging.error(sys.exc_info()[1])
    
    remove(selected_router)

    # updates changed router values in database file
    logging.info("Updating database values for %s." % selected_router)
    try:
        with open(filepath, 'a') as f:
            f.write("{}:{}:{}:{}:{}:{}:{}:{}\n".format(name,router_ip,username,password,backup_status,config_status,backup_date,version))
        logging.info("Database values updated successfully.")
    except:
        logging.error("There was a problem updating the database values. See the error below.")
        logging.error(sys.exc_info()[1])
    