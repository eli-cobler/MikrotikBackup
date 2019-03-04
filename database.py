#
#  database.py
#  MikrotikBackup
#
#
#  Created by Eli Cobler on 01/27/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  This file allows you to add, update, &, remove routers to the Oxidized db file.

import os, shutil
from distutils.dir_util import copy_tree

# paths to database file one for testing local, other for remote server
filepath = os.getcwd() + '/router.db'
#filepath = '/var/MikrotikBackup/router.db'
#filepath = '/home/oxidized/.config/oxidized/router.db'


def get():      
    router_list = []
    # Appends all lines of the file to a list for removal later
    with open(filepath, 'r+') as input:
        for line in input:
            router_list.append(line)
    input.close()

    return router_list

def add(name, router_ip, username, password):
    path = os.getcwd()
    directory_exists = os.path.isdir(path + '/backups/{}'.format(name))
    
    if directory_exists == True:
        return True
    else:
        # writes new router to database file
        with open(filepath, 'a') as f:
            f.write("{}:{}:{}:{}:Not Set:Not Set\n".format(name,router_ip,username,password))
        
        os.mkdir(path + '/backups/{}'.format(name))
        return False

# This function completely removes a router, including the backup files. 
def complete_removal(router):
    router_list = get()
    path = os.getcwd()

    with open(filepath, 'w') as output:
        for item in router_list:
            if router not in item:
                output.write(item)
    output.close()

    shutil.rmtree(path + '/backups/{}'.format(router))

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
def update(name, router_ip, username, password, selected_router, backup_status, config_status, backup_date):
    path = os.getcwd()
    if name != selected_router:
        os.mkdir(path + '/backups/{}'.format(name))
        fromDirectory = path + '/backups/{}'.format(selected_router)
        toDirectory = path + '/backups/{}'.format(name)
        copy_tree(fromDirectory, toDirectory)
        shutil.rmtree(path + '/backups/{}'.format(selected_router))
    
    remove(selected_router)

    # updates changed router values in database file
    with open(filepath, 'a') as f:
        f.write("{}:{}:{}:{}:{}:{}:{}\n".format(name,router_ip,username,password,backup_status,config_status,backup_date))
    