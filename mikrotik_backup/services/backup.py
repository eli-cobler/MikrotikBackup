import datetime, subprocess, sys, logging
import mikrotik_backup.services.router as router
import mikrotik_backup.services.database as database

# server ip 66.76.254.137

# log setup
logging.basicConfig(filename='logs/backup.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def create_backup(router_name, router_ip, username, password):
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
            if backup_output.stdout == '':
                logging.info("Backup ouput completed on router Successfully.")
                print("Backup completed on router Successfully.")

            if backup_output.stdout != '':
                logging.info(backup_output.stdout)
                print("stdout: {}".format(backup_output.stdout))
                #backup_status = backup_output.stdout

            if backup_output.stderr != '':
                logging.warning(backup_output.stderr)
                print("stderr: {}".format(backup_output.stderr))
                #backup_status = backup_output.stderr
        except:
            logging.error(sys.exc_info()[1])
            print("Exception: {}".format(sys.exc_info()[1]))
            #backup_status = sys.exc_info()[1]

        
        try:
            transfer_output = subprocess.run('scp {}@{}:/{} "backups/{}/{}"'.format(username, 
                                                                                    router_ip, 
                                                                                    backup_name, 
                                                                                    router_name, 
                                                                                    backup_name),
                                                                                    shell=True,
                                                                                    universal_newlines=True, 
                                                                                    stdout=subprocess.PIPE, 
                                                                                    stderr=subprocess.PIPE)
            if transfer_output.stdout == '':
                logging.info("Backup transfer completed Successfully.")
                print("Backup transfer completed Successfully.")
                backup_status = "Backup Complete"

            if transfer_output.stdout != '':
                logging.info(transfer_output.stdout)
                print("stdout: {}".format(transfer_output.stdout))

            if transfer_output.stderr != '':
                logging.warning(transfer_output.stderr)
                print("stderr: {}".format(transfer_output.stderr))
        except:
            logging.error(sys.exc_info()[1])
            print("Exception: {}".format(sys.exc_info()[1]))
            
        backup_status = 'Backup Complete'
    except TimeoutError as err:
        print(err)
        #flash(err)
        backup_status = err
    except EOFError as err:
        print(err)
        #flash(err)
        backup_status = err
    except FileNotFoundError as err:
        print(err)
        #flash(err)
        backup_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))
        #flash("{}\n{}".format(the_type, the_value))
        backup_status = the_value

    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')
    database.update(router_name, router_ip, username, password, router_name, backup_status, "Unknown", todays_date, "Unknown")

    return backup_status

def create_config(router_name, router_ip, username, password, backup_status):
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        export_name = date + ".rsc"

        try:
            config_output = subprocess.run('ssh {}@{} export terse > "backups/{}/{}"'.format(username, 
                                                                                            router_ip, 
                                                                                            router_name, 
                                                                                            export_name),
                                                                                            shell=True,
                                                                                            universal_newlines=True, 
                                                                                            stdout=subprocess.PIPE, 
                                                                                            stderr=subprocess.PIPE)

            if config_output.stdout == '':
                logging.info("Config Export Successful.")
                print("Config Export Successful.")
                config_status = 'Config Export Complete'

            if config_output.stdout != '':
                logging.info(config_output.stdout)
                print("stdout: {}".format(config_output.stdout))
                #config_status = config_output.stdout

            if config_output.stderr != '':
                logging.warning(config_output.stderr)
                print("stderr: {}".format(config_output.stdout))
                #config_status = config_output.stderr
        except:
            logging.info(sys.exc_info()[1])
            print("Exception: {}".format(sys.exc_info()[1]))
            #config_status = sys.exc_info()[1]
        
        config_status = 'Config Export Complete'
    except TimeoutError as err:
        print(err)
        #flash(err)
        config_status = err
    except EOFError as err:
        print(err)
        #flash(err)
        config_status = err
    except FileNotFoundError as err:
        print(err)
        #flash(err)
        config_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))
        #flash("{}\n{}".format(the_type, the_value))
        config_status = the_value


    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')
    database.update(router_name, router_ip, username, password, router_name, backup_status, config_status, todays_date, "Unknown")
    
    return config_status

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
            # starting backup
            print("Starting backup for {}...".format(item['router_name']))
            logging.info("Starting backup for %s...", item['router_name'])
            backup_status = create_backup(item['router_name'], item['router_ip'], item['username'], item['password'])
            print("Completed backup for {}".format(item['router_name']))
            logging.info("Completed backup for %s", item['router_name'])

            # starting config export
            print("Starting config export for {}...".format(item['router_name']))
            logging.info("Starting config export for %s...", item['router_name'])
            config_status = create_config(item['router_name'], item['router_ip'], item['username'], item['password'], backup_status)
            print("Config export complete for {}".format(item['router_name']))
            logging.info("Config export complete for %s", item['router_name'])

            # gathering info from rotuers
            router.get_info(item['router_name'], item['router_ip'], item['username'])
            router.parse_info(item['router_name'], item['router_ip'], item['username'], item['password'], backup_status, config_status)
            

if __name__ == "__main__":
    run()