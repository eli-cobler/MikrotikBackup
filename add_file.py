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

# log setup
logging.basicConfig(filename='logs/add_file.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

def ssh_key(username, password, router_ip):
    try:
        # sftping ssh pub key to router
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        logging.info("Transport created")

        print("Attemption connection...")
        logging.info("Attemption connection...")
        transport.connect(username = username, password = password)
        
        print("Sftp created")
        logging.info("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        print("Set remote and local path for transfer...")
        logging.info("Set remote and local path for transfer...")
        remotepath_export = "/id_rsa-2.pub"
        localpath_export = 'id_rsa-2.pub'

        print(f"Trying to place file at {remotepath_export}")
        logging.info(f"Trying to place file at {remotepath_export}.")
        sftp.put(localpath_export, remotepath_export)
        print("SSH Pub Key transfered")
        logging.info("SSH Pub Key transfered")
        
        print("Closing sftp and transport")
        logging.info("Closing sftp and transport")
        sftp.close()
        transport.close()

        print("SSH into router to run import ssh key command")
        logging.info("SSH into router to run import ssh key command")
        # sshing into router to create .backup and export config file
        ssh = paramiko.SSHClient()
        print('Created client')
        logging.info('Created client')

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        logging.info('Set ssh key')

        print('Connecting to router...')
        logging.info('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        logging.info("Connection successful.")
        print("Connection successful.")

        print('Running import command')
        logging.info('Running import command')
        ssh.exec_command(f"/user ssh-keys import public-key-file=id_rsa-2.pub user={username}")
        logging.info("Command successful.")

        print("Closing connection")
        logging.info("Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except paramiko.ssh_exception.SSHException as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except EOFError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except FileNotFoundError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print(f"{the_type}\n{the_value}")
        logging.info("Ran the unexpected error below:")
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
        logging.info("Transport created")
        
        print("Attemption connection...")
        logging.info("Attemption connection...")
        transport.connect(username = username, password = password)
        
        print("Sftp created")
        logging.info("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        logging.info("Set remote and local path")
        print("Set remote and local path")
        remotepath = "/autoUpdater.rsc"
        localpath = 'autoUpdater.rsc'
        
        print("Transfering Script...")
        logging.info("Transfering Script...")
        sftp.put(localpath, remotepath)
        print("Script transfered.")
        logging.info("Script transfered.")
        
        print("Closing sftp and transport")
        logging.info("Closing sftp and transport")
        sftp.close()
        transport.close()

        # creating script and scheduler
        print("Creating Autoupdate script and scheduler...")
        logging.info("Creating Autoupdate script and scheduler...")
        
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
        logging.info("Commands successful")

        print("Closing connection")
        logging.info("Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except paramiko.ssh_exception.SSHException as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except EOFError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
        logging.info("Ran the error below:")
        logging.error(err)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print(f"{the_type}\n{the_value}")
        logging.info("Ran the unexpected error below:")
        logging.error(the_type, the_value)
