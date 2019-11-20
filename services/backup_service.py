import datetime
import logging
import os
import subprocess
import sys

from tqdm import tqdm

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
import data.db_session as db_session
from data.router import Router
from services import router_service, router_details_service

# log setup
logging.basicConfig(filename='logs/backup.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


def create_backup(router_name, router_ip, username):
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        backup_name = date + ".backup"

        try:
            backup_output = subprocess.run('ssh {}@{} /system backup save name={}'.format(username,
                                                                                          router_ip,
                                                                                          backup_name),
                                           shell=True,
                                           universal_newlines=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if backup_output.stdout != '':
                logging.info(backup_output.stdout)
                tqdm.write("stdout: {}".format(backup_output.stdout))
                # backup_status = backup_output.stdout

            if backup_output.stderr != '':
                logging.warning(backup_output.stderr)
                tqdm.write("stderr: {}".format(backup_output.stderr))
                # backup_status = backup_output.stderr
        except:
            logging.error(sys.exc_info()[1])
            tqdm.write("Exception: {}".format(sys.exc_info()[1]))
            # backup_status = sys.exc_info()[1]

        try:
            top_folder = os.path.dirname(__file__)
            rel_folder = os.path.join('..', 'backups')
            backups_path = os.path.abspath(os.path.join(top_folder, rel_folder))
            transfer_output = subprocess.run('scp {}@{}:/{} "{}/{}/{}"'.format(username,
                                                                                router_ip,
                                                                                backup_name,
                                                                                backups_path,
                                                                                router_name,
                                                                                backup_name),
                                             shell=True,
                                             universal_newlines=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
            if transfer_output.stdout != '':
                logging.info(transfer_output.stdout)
                tqdm.write("stdout: {}".format(transfer_output.stdout))

            if transfer_output.stderr != '':
                logging.warning(transfer_output.stderr)
                tqdm.write("stderr: {}".format(transfer_output.stderr))
        except:
            logging.error(sys.exc_info()[1])
            tqdm.write("Exception: {}".format(sys.exc_info()[1]))

        backup_status = 'Backup Complete'
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
        tqdm.write("{}\n{}".format(the_type, the_value))
        backup_status = the_value

    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')

    # updating database values in sql database
    session = db_session.create_session()
    r = session.query(Router).filter(Router.router_name == router_name).one()
    r.backup_status = backup_status
    r.last_attempted = todays_date
    session.commit()

    return backup_status


def create_config(router_name, router_ip, username):
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        export_name = date + ".rsc"

        try:
            top_folder = os.path.dirname(__file__)
            rel_folder = os.path.join('..', 'backups')
            backups_path = os.path.abspath(os.path.join(top_folder, rel_folder))
            config_output = subprocess.run('ssh {}@{} export terse > "{}/{}/{}"'.format(username,
                                                                                        router_ip,
                                                                                        backups_path,
                                                                                        router_name,
                                                                                        export_name),
                                           shell=True,
                                           universal_newlines=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if config_output.stdout != '':
                logging.info(config_output.stdout)
                tqdm.write("stdout: {}".format(config_output.stdout))
                # config_status = config_output.stdout

            if config_output.stderr != '':
                logging.warning(config_output.stderr)
                tqdm.write("stderr: {}".format(config_output.stdout))
                # config_status = config_output.stderr
        except:
            logging.info(sys.exc_info()[1])
            tqdm.write("Exception: {}".format(sys.exc_info()[1]))
            # config_status = sys.exc_info()[1]

        config_status = 'Config Export Complete'
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
        tqdm.write("{}\n{}".format(the_type, the_value))
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

    for item in tqdm(routers, total=router_count, unit=" router"):
        if item.router_name in ignore_list:
            logging.info("Backup skipped for %s" % item.router_name)
            tqdm.write("Backup skipped for {}".format(item.router_name))
        else:
            # starting backup
            tqdm.write("Starting backup for {}...".format(item.router_name))
            logging.info("Starting backup for %s..." % item.router_name)
            backup_status = create_backup(item.router_name, item.router_ip, item.username)
            tqdm.write("Completed backup for {}".format(item.router_name))
            logging.info("Completed backup for %s" % item.router_name)

            # starting config export
            # tqdm.write("Starting config export for {}...".format(item['router_name']))
            tqdm.write("Starting config export for {}...".format(item.router_name))
            logging.info("Starting config export for %s..." % item.router_name)
            config_status = create_config(item.router_name, item.router_ip, item.username)
            # tqdm.write("Config export complete for {}".format(item['router_name']))
            tqdm.write("Config export complete for {}".format(item.router_name))
            logging.info("Config export complete for %s" % item.router_name)

            # gathering info from rotuers
            router_details_service.get_info(item.router_name, item.router_ip, item.username)
            router_details_service.parse_info(item.router_name)


if __name__ == "__main__":
    init_db()
    run()