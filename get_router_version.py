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
    #print(router_info.stdout)

    # paths to router info file 
    filepath = 'router_info/{}.txt'.format(router_name)
    with open(filepath, 'w') as f:
        f.write(router_info.stdout)



if __name__ == "__main__":
    router_name = input('Router Name: ')
    router_ip = input('Router IP: ')
    username = input('Username: ')
    get_info(router_name, router_ip, username)
