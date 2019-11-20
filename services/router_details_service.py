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

import subprocess, os, logging, sys
from tqdm import tqdm
from data import db_session
from data.router import Router
from services import router_service

# log setup
top_folder = os.path.dirname(__file__)
rel_file = os.path.join('..','logs','get_router_version.log')
log_file = os.path.abspath(os.path.join(top_folder, rel_file))
logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def main():
    init_db()
    run()

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..','db','mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

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

        top_folder = os.path.dirname(__file__)
        rel_folder = os.path.join('..', 'router_info', router_name + '.txt')
        filepath = os.path.abspath(os.path.join(top_folder, rel_folder))
        with open(filepath, 'w+') as f:
            f.write(router_info.stdout)
        
        logging.info("Info saved.")
        tqdm.write("Info saved.")
    except:
        logging.error(sys.exc_info()[1])
        tqdm.write("Exception: {}".format(sys.exc_info()[1]))

def parse_info(router_name):

    # setting up db session and making query for update
    session = db_session.create_session()
    r = session.query(Router).filter(Router.router_name == router_name).one()

    top_folder = os.path.dirname(__file__)
    rel_folder = os.path.join('..', 'router_info', router_name + '.txt')
    filepath = os.path.abspath(os.path.join(top_folder, rel_folder))
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'uptime' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                uptime = cleaned_data[1]
                tqdm.write("{} uptime: {}".format(router_name, uptime))
                logging.info(f'{router_name} uptime: {uptime}')
                r.uptime = uptime

            if 'version' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                router_os = cleaned_data[1]
                tqdm.write("{}: {}".format(router_name,router_os))
                logging.info(f'{router_name} has a RouterOS: {router_os}')
                r.router_os_version = router_os

            if 'free-memory' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                free_memory = cleaned_data[1]
                tqdm.write("{} free_memory: {}".format(router_name, free_memory))
                logging.info(f'{router_name} free_memory: {free_memory}')
                r.free_memory = free_memory

            if 'total-memory' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                total_memory = cleaned_data[1]
                tqdm.write("{} total_memory: {}".format(router_name, total_memory))
                logging.info(f'{router_name} total_memory: {total_memory}')
                r.total_memory = total_memory

            if 'cpu-load' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                cpu_load = cleaned_data[1]
                tqdm.write("{} cpu_load: {}".format(router_name, cpu_load))
                logging.info(f'{router_name} cpu_load: {cpu_load}')
                r.cpu_load = cpu_load

            if 'free-hdd-space' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                free_hdd_space = cleaned_data[1]
                tqdm.write("{} free_hdd_space: {}".format(router_name, free_hdd_space))
                logging.info(f'{router_name} free_hdd_space: {free_hdd_space}')
                r.free_hdd_space = free_hdd_space

            if 'total-hdd-space' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                total_hdd_space = cleaned_data[1]
                tqdm.write("{} total_hdd_space: {}".format(router_name, total_hdd_space))
                logging.info(f'{router_name} total_hdd_space: {total_hdd_space}')
                r.total_hdd_space = total_hdd_space

            if 'bad-blocks' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                bad_blocks = cleaned_data[1]
                tqdm.write("{} bad_blocks: {}".format(router_name, bad_blocks))
                logging.info(f'{router_name} bad_blocks: {bad_blocks}')
                r.bad_blocks = bad_blocks

            if 'board-name' in line:
                data = line.split(':')
                cleaned_data = data[1].split(' ')
                board_name = cleaned_data[1]
                tqdm.write("{} board_name: {}".format(router_name, board_name))
                logging.info(f'{router_name} board_name: {board_name}')
                r.board_name = board_name


    # committing changes to the db
    session.commit()


def run():
    ignore_list = ['Spectrum Voice',
                   'CASA',
                   'Value Med Midwest City',
                   'Valu Med Harrah',
                   'Value Med FTG',
                   'GPSS Hobart',
                   'Farmers Caleb Conner',
                   'Farmers Wayne Buck',
                   'GPSS HQ']

    routers = router_service.get_router_list()

    router_count = 0
    for r in routers:
        router_count += 1

    for r in tqdm(routers, total=router_count, unit=" router"):
        if r.router_name in ignore_list:
            logging.info("Gathering info skipped for %s", r.router_name)
            tqdm.write("Gathering info skipped for " + r.router_name)
        else:
            parse_info(r.router_name)

    
if __name__ == "__main__":
    main()