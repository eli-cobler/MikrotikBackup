import logging
from tqdm import tqdm
from MikrotikBackup.services import backup_service, router_details_service


def run(router_name,router_ip,username):
    backup_service.init_db()

    # starting backup
    tqdm.write(f"Starting backup for {router_name}...")
    logging.info(f"Starting backup for {router_name}...")
    backup_status = backup_service.create_backup(router_name, router_ip, username)
    tqdm.write(f"Completed backup for {router_name}")
    logging.info(f"Completed backup for {router_name}")

    # starting config export
    # tqdm.write("Starting config export for {}...".format('router_name']))
    tqdm.write(f"Starting config export for {router_name}...")
    logging.info(f"Starting config export for {router_name}...")
    config_status = backup_service.create_config(router_name, router_ip, username)
    # tqdm.write("Config export complete for {}".format('router_name']))
    tqdm.write(f"Config export complete for {router_name}")
    logging.info(f"Config export complete for {router_name}")

    # gathering info from rotuers
    router_details_service.get_info(router_name, router_ip, username)
    router_details_service.parse_info(router_name)


