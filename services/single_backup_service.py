import logging
from tqdm import tqdm
from services import router_details_service, backup_service

def run(router_name,router_ip,username):
    backup_service.init_db()

    # starting backup
    tqdm.write("Starting backup for {}...".format(router_name))
    logging.info("Starting backup for %s..." % router_name)
    backup_status = backup_service.create_backup(router_name, router_ip, username)
    tqdm.write("Completed backup for {}".format(router_name))
    logging.info("Completed backup for %s" % router_name)

    # starting config export
    # tqdm.write("Starting config export for {}...".format('router_name']))
    tqdm.write("Starting config export for {}...".format(router_name))
    logging.info("Starting config export for %s..." % router_name)
    config_status = backup_service.create_config(router_name, router_ip, username)
    # tqdm.write("Config export complete for {}".format('router_name']))
    tqdm.write("Config export complete for {}".format(router_name))
    logging.info("Config export complete for %s" % router_name)

    # gathering info from rotuers
    router_details_service.get_info(router_name, router_ip, username)
    router_details_service.parse_info(router_name)


