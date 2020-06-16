#
#   removeBackupFiles.py
#   MikrotikBakcup
#
#   Created by Eli Cobler on 06/13/19.
#   Copyright © 2018 Eli Cobler. All rights reserved.
#
#   This project allows you generate and store backup and config
#  files from Mikrotik Routers.
#
#   This file removes all backup files from the router keeping them from filling up on backups.

# python module imports
import os,logging,sys, subprocess
from tqdm import tqdm

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

# project module imports
import data.db_session as db_session
from services import router_service

# log setup
logging.basicConfig(filename='logs/removeBackupFiles.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


def run():
    tqdm.write("Gathering Routers...")
    logging.info("Gathering Routers...")

    ignore_list = router_service.get_router_ignore_list()
    router_list = router_service.get_router_list()
    router_count = router_service.get_router_count()

    tqdm.write("Routers Gathered.")
    logging.info("Routers Gathered.")

    for item in tqdm(router_list, total=router_count, unit=" routers"):
        tqdm.write(f"Starting Removal for {item.router_name}...")
        logging.info(f"Starting Removal for {item.router_name}...")

        if item.router_name in ignore_list:
            tqdm.write("Removal skipped.")
            logging.info("Removal skipped.")
        else:
            try:
                remove_backup = subprocess.run(f'ssh {item.username}@{item.router_ip} /file remove [find type="backup"]',
                                               shell=True,
                                               universal_newlines=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                if remove_backup.stdout != '':
                    logging.info(remove_backup.stdout)
                    tqdm.write(f"stdout: {remove_backup.stdout}")

                if remove_backup.stderr != '':
                    logging.warning(remove_backup.stderr)
                    tqdm.write(f"stderr: {remove_backup.stderr}")
            except:
                logging.error(sys.exc_info()[1])
                tqdm.write(f"Exception: {sys.exc_info()[1]}")

            tqdm.write(f"Removal for {item.router_name} completed.")
            logging.info(f"Removal for {item.router_name} completed.")



if __name__ == "__main__":
    init_db()
    run()