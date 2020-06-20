import asyncio
import datetime
import logging
import os
import sys
import colorama

from tqdm import tqdm

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
import mikrotik_backup.data.db_session as db_session
from mikrotik_backup.data.router import Router
from mikrotik_backup.services import router_details_service, router_service

# log setup
logging.basicConfig(filename='logs/backup.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('../..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

async def create_backup(router_name, router_ip, username):
    global backup_status
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        backup_name = date + ".backup"

        try:
            backup_output = await asyncio.create_subprocess_shell('ssh {}@{} /system backup save name={}'.format(username,
                                                                                                                  router_ip,
                                                                                                                  backup_name),
                                                                                                                  stdout=asyncio.subprocess.PIPE,
                                                                                                                  stderr=asyncio.subprocess.PIPE)

            try:
                tqdm.write(f'Starting transfer for {router_name}')
                top_folder = os.path.dirname(__file__)
                rel_folder = os.path.join('../..', 'backups')
                backups_path = os.path.abspath(os.path.join(top_folder, rel_folder))
                transfer_output = await asyncio.create_subprocess_shell('scp {}@{}:/{} "{}/{}/{}"'.format(username,
                                                                                                            router_ip,
                                                                                                            backup_name,
                                                                                                            backups_path,
                                                                                                            router_name,
                                                                                                            backup_name),
                                                                                                            stdout=asyncio.subprocess.PIPE,
                                                                                                            stderr=asyncio.subprocess.PIPE)
                if transfer_output.stdout == '':
                    logging.info(transfer_output.stdout)
                    backup_status = "Backup Complete"
                elif transfer_output.stdout != '':
                    logging.info(transfer_output.stdout)
                    backup_status = transfer_output.stdout

                if transfer_output.stderr != '':
                    logging.warning(transfer_output.stderr)
                    tqdm.write(f"transfer stderr: {transfer_output.stderr}")


            except:
                logging.error(sys.exc_info()[1])
                tqdm.write(f"Exception: {sys.exc_info()[1]}")
                #backup_status = sys.exc_info()[1]


            if backup_output.stderr != '':
                logging.warning(backup_output.stderr)
                tqdm.write(f"stderr: {backup_output.stderr}")
                backup_status = backup_output.stderr

        except:
            the_type, the_value, the_traceback = sys.exc_info()
            tqdm.write(f"{the_type}\n{the_value}")
            #backup_status = the_value

        #backup_status = 'Backup Complete'
    except TimeoutError as err:
        tqdm.write(err)
        backup_status = err
    except EOFError as err:
        tqdm.write(err)
        backup_status = err
    except FileNotFoundError as err:
        tqdm.write(err)
        backup_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        tqdm.write(f"{the_type}\n{the_value}")
        backup_status = the_value

    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')

    # updating database values
    session = db_session.create_session()
    r = session.query(Router).filter(Router.router_name == router_name).one()
    r.backup_status = backup_status
    r.last_attempted = todays_date
    session.commit()

    return backup_status

async def create_config(router_name, router_ip, username):
    global config_status
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        export_name = date + ".rsc"

        try:
            top_folder = os.path.dirname(__file__)
            rel_folder = os.path.join('../..', 'backups')
            backups_path = os.path.abspath(os.path.join(top_folder, rel_folder))
            config_output = await asyncio.create_subprocess_shell('ssh {}@{} export terse > "{}/{}/{}"'.format(username,
                                                                                                                router_ip,
                                                                                                                backups_path,
                                                                                                                router_name,
                                                                                                                export_name),
                                                                                                                stdout = asyncio.subprocess.PIPE,
                                                                                                                stderr = asyncio.subprocess.PIPE)
            if config_output.stdout == '':
                logging.info(config_output.stdout)
                config_status = "Config Complete"
            elif config_output.stdout != '':
                logging.info(config_output.stdout)
                config_status = config_output.stdout

            if config_output.stderr != '':
                logging.warning(config_output.stderr)
                config_status = config_output.stderr
        except:
            logging.info(sys.exc_info()[1])
            tqdm.write(f"Exception: {sys.exc_info()[1]}")
            # config_status = sys.exc_info()[1]

        #config_status = 'Config Export Complete'
    except TimeoutError as err:
        tqdm.write(err)
        # flash(err)
        config_status = err
    except EOFError as err:
        tqdm.write(err)
        # flash(err)
        config_status = err
    except FileNotFoundError as err:
        tqdm.write(err)
        # flash(err)
        config_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        tqdm.write(f"{the_type}\n{the_value}")
        # flash("{}\n{}".format(the_type, the_value))
        config_status = the_value

    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')

    # updating database values
    session = db_session.create_session()
    r = session.query(Router).filter(Router.router_name == router_name).one()
    r.config_status = config_status
    r.last_attempted = todays_date
    session.commit()

    return config_status

def run():
    # setting start time for sync to async comparison
    start_time = datetime.datetime.now()

    # gathering list all routers and list of routers to be ignored and router count
    routers = router_service.get_router_list()
    ignored_routers = router_service.get_router_ignore_list()
    router_count = router_service.get_router_count()

    loop = asyncio.get_event_loop()

    for item in tqdm(routers, total=router_count, unit=" router"):
        if item.router_name in ignored_routers:
            logging.info(f"Backup skipped for {item.router_name}")
            tqdm.write(f"Backup skipped for {item.router_name}")
            backup_status = "Backup Skipped"
            config_status = "Config Skipped"

            session = db_session.create_session()
            r = session.query(Router).filter(Router.router_name == item.router_name).one()
            r.backup_status = backup_status
            r.config_status = config_status
            session.commit()
        else:
            # starting backup
            tqdm.write(f"Starting backup for {item.router_name}...")
            logging.info(f"Starting backup for {item.router_name}...")

            task_1 = loop.create_task(create_backup(item.router_name, item.router_ip, item.username))

            # backup file completed
            tqdm.write(f"Completed backup for {item.router_name}")
            logging.info(f"Completed backup for {item.router_name}")


            # starting config export
            tqdm.write(f"Starting config export for {item.router_name}...")
            logging.info(f"Starting config export for {item.router_name}...")

            task_2 = loop.create_task(create_config(item.router_name, item.router_ip, item.username))

            tqdm.write(f"Config export complete for {item.router_name}")
            logging.info(f"Config export complete for {item.router_name}")

            # gathering info from rotuers
            task_3 = loop.create_task(router_details_service.get_info(item.router_name, item.router_ip, item.username))
            router_details_service.parse_info(item.router_name)

            final_task = asyncio.gather(task_1, task_2, task_3)

            loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - start_time
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)

if __name__ == "__main__":
    init_db()
    run()