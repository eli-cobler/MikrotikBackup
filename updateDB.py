#
#  update.py
#  MikrotikBackup
#
#  Created by Eli Cobler on 11/18/18.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router backup.
#
#  This file allows you to add & remove routers to the db file.


def add(name, router_ip, username, password):
    with open("/home/oxidized/.config/oxidized/router.db", 'a') as f: 
        f.write("{}:{}:routeros:{}:{}:enable_password\n".format(name, router_ip, username, password))           # writes new router to database file   


def remove(this):                                                               # This function reads each line in the database file then removes the 
    filepath = '/Users/coblere/Documents/GitHub/MikrotikBackup/router.db'       # the desired line by overwriting the entire file omitting the desired line.      
    line_list = []
    with open(filepath, 'r+') as input:                                         # Appends all lines of the file to a list for removal later
        for line in input:                                                      # Yes I know this isn't the best/fastest way to do this but it was the first
            line_list.append(line)                                              # way it worked for me. So I will optimize this at a later date.
    input.close()
        
    with open(filepath, 'w') as output:
        for item in line_list:
            if this not in item:                                                # If the line does not have the name of the router we want to remove then it
                output.write(item)                                              # is written back to the db file. 
    output.close()