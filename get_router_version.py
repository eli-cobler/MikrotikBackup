#
#  get_router_version
#  Mikrotik Backup
#
#  Created by Eli Cobler on 08/08/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  Gets the current version of router OS running on the router. 

import subprocess, database, os, logging, paramiko



# log setup
logging.basicConfig(filename='logs/get_router_version.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def get_info(router_name,router_ip, username):
    print('Gathering info for {}...'.format(router_name))
    logging.info('Gathering info for {}...'.format(router_name))
    # sshing into router to get router OS verison
    print('Running system info command')
    logging.info('Running system info command')
    router_info = subprocess.run('ssh {}@{} /system resource print'.format(username, 
                                                                    router_ip),
                                                                    shell=True,
                                                                    universal_newlines=True,
                                                                    stdout=subprocess.PIPE,
                                                                    stderr=subprocess.PIPE)
    logging.info("Info gatherered for {}".format(router_name))
    print("Info gatherered for {}".format(router_name))

    # paths to router info file 
    logging.info("Saving info to file.")
    print(("Saving info to file."))
    filepath = 'router_info/{}.txt'.format(router_name)
    with open(filepath, 'w') as f:
        f.write(router_info.stdout)
    
    logging.info("Info saved.")
    print("Info saved.")

def run():
    ignore_list = ['Spectrum Voice',
                    'CASA',
                    'Value Med Midwest City',
                    'Valu Med Harrah', 
                    'Value Med FTG',
                    'GPSS Hobart']
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
        if item['router_name'] in ignore_list:
            logging.info("Backup skipped for %s", item['router_name'])
        else:
            get_info(item['router_name'], item['router_ip'], item['username'])

if __name__ == "__main__":
    run()

    
