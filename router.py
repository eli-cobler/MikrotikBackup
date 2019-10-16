#
#  get_router_version
#  Mikrotik Backup
#
#  Created by Eli Cobler on 08/08/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you generate and store backup and config
#  files from Mikrotik Routers. 
#
#  Gets the current version of routerOS running on the router. 

import subprocess, database, os, logging, sys, datetime
from tqdm import tqdm
# log setup

logging.basicConfig(filename='logs/get_router_version.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def get_info(router_name,router_ip, username):
    tqdm.write('Gathering info for {}...'.format(router_name))
    logging.info('Gathering info for {}...'.format(router_name))
    # sshing into router to get router OS verison
    tqdm.write('Running system info command')
    logging.info('Running system info command')
    
    try:
        router_info = subprocess.run('ssh {}@{} /system resource print'.format(username,
                                                                        router_ip),
                                                                        shell=True,
                                                                        universal_newlines=True,
                                                                        stdout=subprocess.PIPE,
                                                                        stderr=subprocess.PIPE)
        logging.info("Info gatherered for {}".format(router_name))
        tqdm.write("Info gatherered for {}".format(router_name))

        # paths to router info file 
        logging.info("Saving info to file.")
        tqdm.write("Saving info to file.")
        filepath = 'router_info/{}.txt'.format(router_name)
        with open(filepath, 'w+') as f:
            f.write(router_info.stdout)
        
        logging.info("Info saved.")
        tqdm.write("Info saved.")
    except:
        logging.error(sys.exc_info()[1])
        tqdm.write("Exception: {}".format(sys.exc_info()[1]))

def parse_info(router_name,router_ip,username,password,backup_status,config_status):
    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')
    filepath = 'router_info/{}.txt'.format(router_name)
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'version' in line:
                data = line.split(':')
                version = data[1].split(' ')
                router_os = version[1]
                release_type = version[2]
                tqdm.write("{}: {}".format(router_name,router_os))
                logging.info(f'{router_name} has a RouterOS: {router_os}')
                database.update(router_name,router_ip,username,password,router_name,backup_status,config_status,todays_date,router_os)

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
            logging.info("Gathering info skipped for %s", item['router_name'])
            tqdm.write("Gathering info skipped for " + item['router_name'])
        else:
            #get_info(item['router_name'], item['router_ip'], item['username'])
            parse_info(item['router_name'],item['router_ip'],item['username'],item['password'],"Not set","Not Set")

    
#if __name__ == "__main__":
#    run()