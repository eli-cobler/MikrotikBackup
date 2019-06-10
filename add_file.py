import subprocess, datetime, paramiko, database, sys

def ssh_key(username, password, router_ip):
    try:
        # sftping ssh pub key to router
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path for transfer...")
        remotepath_export = "/id_rsa-2.pub"
        localpath_export = 'id_rsa-2.pub'
        #/Users/coblere/Documents/GitHub/MikrotikBackup/backups/Aces
        print("Trying to place file at {}".format(remotepath_export))
        sftp.put(localpath_export, remotepath_export)
        print("SSH Pub Key transfered")
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        print("SSH into router to run import ssh key command")
        # sshing into router to create .backup and export config file
        ssh = paramiko.SSHClient()
        print('Created client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        print('Running import command')
        #/user ssh-keys import public-key-file=mykey.pub user=admin
        ssh.exec_command("/user ssh-keys import public-key-file=id_rsa-2.pub user=admin")
        print("Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(err)
    except paramiko.ssh_exception.SSHException as err:
        print(err)
    except EOFError as err:
        print(err)
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))

def remove_Backup_Files(username, password, router_ip):
    try:
        # sftping ssh pub key to router
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path for transfer...")
        remotepath_export = "/removeBackupFiles.rsc"
        localpath_export = 'removeBackupFiles.rsc'
        #/Users/coblere/Documents/GitHub/MikrotikBackup/backups/Aces
        print("Trying to place file at {}".format(remotepath_export))
        sftp.put(localpath_export, remotepath_export)
        print("SSH Pub Key transfered")
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        print("SSH into router to run import ssh key command")
        # sshing into router to create .backup and export config file
        ssh = paramiko.SSHClient()
        print('Created client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        print('Running import command')
        #/user ssh-keys import public-key-file=mykey.pub user=admin
        ssh.exec_command("/user ssh-keys import public-key-file=id_rsa-2.pub user=admin")
        print("Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(err)
    except paramiko.ssh_exception.SSHException as err:
        print(err)
    except EOFError as err:
        print(err)
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))

def autoUpdater(router_name, router_ip, username, password):

    today = datetime.datetime.today() 
    tomorrow = today + datetime.timedelta(1)

    print("Trying to connect to {}".format(router_name))
    try: 
        # sftping script to router
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path")
        remotepath = "/autoUpdater.rsc"
        localpath = 'autoUpdater.rsc'
        print("Transfering Script...")
        sftp.put(localpath, remotepath)
        print("Script transfered.")
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        # creating script and scheduler
        print("Creating Autoupdate script and scheduler...")
        ssh = paramiko.SSHClient()
        print('Created client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password, look_for_keys=False)
        print('Running commands...')
        ssh.exec_command('/system script add name=autoupdate policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="/import file-name=autoUpdater.rsc"')
        ssh.exec_command('/system scheduler add name=AutoUpdate interval=24h start-time=02:30:00 on-event=autoupdate start-date={}'.format(tomorrow.strftime('%b/%d/%Y')))
        print("Closing connection")
        ssh.close()
    except TimeoutError as err:
        print(err)
    except paramiko.ssh_exception.SSHException as err:
        print(err)
    except EOFError as err:
        print(err)
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))

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
            ssh_key(item['username'], item['password'], item['router_ip'])
