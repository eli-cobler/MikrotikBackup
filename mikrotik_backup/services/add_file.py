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

import datetime, paramiko, sys, logging, os

current_directory = os.getcwd()
sys.path.insert(1,current_directory.replace('/mikrotik_backup',''))
import mikrotik_backup.services.database as database


# log setup
logging.basicConfig(filename='mikrotik_backup/logs/add_file.log',
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
        localpath_export = 'mikrotik_backup/resources/id_rsa-2.pub'

        print("Trying to place file at {}".format(remotepath_export))
        logging.info("Trying to place file at %s." % remotepath_export)
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
        ssh.exec_command("/user ssh-keys import public-key-file=id_rsa-2.pub user={}".format(username))
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
        print("{}\n{}".format(the_type, the_value))
        logging.info("Ran into unexpected error")

def autoUpdater(router_name, router_ip, username, password):

    today = datetime.datetime.today() 
    tomorrow = today + datetime.timedelta(1)

    print("Trying to connect to {}".format(router_name))
    logging.info("Trying to connect to %s" % router_name)
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
        localpath = 'mikrotik_backup/resources/autoUpdater.rsc'
        
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
        ssh.exec_command('/system scheduler add name=AutoUpdate interval=24h start-time=02:30:00 on-event=autoupdate start-date={}'.format(tomorrow.strftime('%b/%d/%Y')))
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
        print("{}\n{}".format(the_type, the_value))
        logging.info("Ran into unexpected error")

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
        if item['router_name'] == 'Aces' or item['router_name'] == 'Arrowhead Mall' or item['router_name'] == 'FBC Wagoner':
            pass
        else:
            print("Starting {}...".format(item['router_name']))
            logging.info("Starting %s..." % item['router_name'])
            ssh_key(item['username'], item['password'], item['router_ip'])
            print("{} finished.".format(item['router_name']))
            logging.info("%s finished." % item['router_name'])
