import datetime, paramiko, subprocess, database, os, schedule, time

def add(router_name, router_ip, username, password):

    today = datetime.datetime.today() 
    tomorrow = today + datetime.timedelta(1)
    currentPath = os.path.dirname(os.path.realpath(__file__))
    print(currentPath)

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
        ssh.connect(router_ip, username=username, password=password)
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
    #except:
    #    print("Unexpected Error.")

add('eConstruct USA (Orlando)', '75.58.178.237', 'admin', 'Admin1@3')