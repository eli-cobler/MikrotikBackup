#
#  add_file.py
#  MikrotikBakcup
#
#  Created by Eli Cobler on 06/13/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  This file is used to add the various files needed on the routers like ssh key's and the auto 
#  updater script.

import datetime, paramiko, sys, logging
from datetime import datetime as date

# log setup
log_date_time = date.now().strftime("%m-%d-%Y %H:%M:%S")

def ssh_key(username, password, router_ip):
    try:
        # sftping ssh pub key to router
        transport = paramiko.Transport((router_ip))
        print(f"{log_date_time} Transport created")

        print(f"{log_date_time} Attemption connection...")
        transport.connect(username = username, password = password)

        print(f"{log_date_time} Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)

        print(f"{log_date_time} Set remote and local path for transfer...")
        remotepath_export = "/id_rsa-2.pub"
        localpath_export = 'id_rsa-2.pub'

        print(f"{log_date_time} Trying to place file at {remotepath_export}")
        sftp.put(localpath_export, remotepath_export)
        print(f"{log_date_time} SSH Pub Key transfered")

        print(f"{log_date_time} Closing sftp and transport")
        sftp.close()
        transport.close()

        print(f"{log_date_time} SSH into router to run import ssh key command")
        # sshing into router to create .backup and export config file
        ssh = paramiko.SSHClient()
        logging.info('Created client')

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"{log_date_time} Set ssh key")

        print(f"{log_date_time} Connecting to router...")
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        print(f"{log_date_time} Connection successful.")

        print(f"{log_date_time} Running import command")
        ssh.exec_command(f"/user ssh-keys import public-key-file=id_rsa-2.pub user={username}")
        print(f"{log_date_time} Command successful.")

        print(f"{log_date_time} Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except paramiko.ssh_exception.SSHException as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except EOFError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except FileNotFoundError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print(f"{the_type}\n{the_value}")
        print(f"{log_date_time} Ran the unexpected error below:")
        logging.error(the_type,the_value)

def autoUpdater(router_name, router_ip, username, password):

    today = datetime.datetime.today() 
    tomorrow = today + datetime.timedelta(1)

    print(f"Trying to connect to {router_name}")
    logging.info(f"Trying to connect to {router_name}")
    try: 
        # sftping script to router
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print(f"{log_date_time} Transport created")
        
        print("Attemption connection...")
        print(f"{log_date_time} Attemption connection...")
        transport.connect(username = username, password = password)
        
        print("Sftp created")
        print(f"{log_date_time} Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        print(f"{log_date_time} Set remote and local path")
        print("Set remote and local path")
        remotepath = "/autoUpdater.rsc"
        localpath = 'autoUpdater.rsc'
        
        print("Transfering Script...")
        print(f"{log_date_time} Transfering Script...")
        sftp.put(localpath, remotepath)
        print("Script transfered.")
        print(f"{log_date_time} Script transfered.")
        
        print("Closing sftp and transport")
        print(f"{log_date_time} Closing sftp and transport")
        sftp.close()
        transport.close()

        # creating script and scheduler
        print("Creating Autoupdate script and scheduler...")
        print(f"{log_date_time} Creating Autoupdate script and scheduler...")
        
        ssh = paramiko.SSHClient()
        print('Created client')
        logging.info('Created client')
        
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        logging.info('Set ssh key')
        
        print('Connecting to router...')
        logging.info('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        
        print('Running commands...')
        logging.info('Running commands...')
        ssh.exec_command('/system script add name=autoupdate policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="/import file-name=autoUpdater.rsc"')
        ssh.exec_command(f"/system scheduler add name=AutoUpdate interval=24h start-time=02:30:00 on-event=autoupdate start-date={tomorrow.strftime('%b/%d/%Y')}")
        print("Commands successful")
        print(f"{log_date_time} Commands successful")

        print("Closing connection")
        print(f"{log_date_time} Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except paramiko.ssh_exception.SSHException as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except EOFError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(f"{log_date_time} Ran the error below:\n {err}")
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print(f"{log_date_time} {the_type}\n{the_value}")
        print(f"{log_date_time} Ran the unexpected error below:\n {the_type} {the_value}")
