import datetime, paramiko, subprocess, database, os, schedule, time, sys
from datetime import date 
# office ip 47.217.151.73
# home ip 47.217.140.46
# roberts home ip 66.76.254.137

def create_backup(router_name, router_ip, username, password):
    # getting current date and time for naming backup file
    date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
    filename = date + ".backup"

    try:
        # sshing into router to create .backup and export config file
        print("Generating backup for {}...".format(router_name))
        ssh = paramiko.SSHClient()
        print('Created client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password)
        print('Running backup command')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/system backup save name={}".format(date))
        print("Closing connection")
        ssh.close()

        # sftping backup and exported config file from router to server
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path for backup file...")
        remotepath_backup = "/{}".format(filename)
        localpath_backup = 'backups/{}/{}'.format(router_name,filename)
        print("Backup transfered")
        sftp.get(remotepath_backup, localpath_backup)
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        # sshing back into router to remove .backup and exported config file
        ssh = paramiko.SSHClient()
        print('Created client')  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password)
        print('Running remove backup command')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/file remove "{}"'.format(filename))
        print("Closing connection")    
        ssh.close()
        print("Backup for {} complete.".format(router_name))
        backup_status = "Backup Completed"
    except TimeoutError as err:
        print(err)
        backup_status = err
    except paramiko.ssh_exception.SSHException as err:
        print(err)
        backup_status = err
    except EOFError as err:
        print(err)
        backup_status = err
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
        backup_status = err
    except FileNotFoundError as err:
        print(err)
        backup_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))
        backup_status = the_value

    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')
    database.update(router_name,router_ip,username,password,router_name,backup_status, "Not Set", todays_date)

    return backup_status

def create_config(router_name, router_ip, username, password, backup_status):
    # getting current date and time for naming backup file
    date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
    export_name = date + ".rsc"

    try:
        print("Generating Config for {}...".format(router_name))
        # sshing into router to create .backup and export config file
        ssh = paramiko.SSHClient()
        print('Created client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password)
        print('Running export command')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("export file={}".format(date))
        print("Closing connection")
        ssh.close()

        # sftping backup and exported config file from router to server
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path for exported config...")
        remotepath_export = "/{}".format(export_name)
        localpath_export = 'backups/{}/{}'.format(router_name,export_name)
        print("Exported config transfered")
        sftp.get(remotepath_export, localpath_export)
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        # sshing back into router to remove .backup and exported config file
        ssh = paramiko.SSHClient()
        print('Created client')  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Set ssh key')
        print('Connecting to router...')
        ssh.connect(router_ip, username=username, password=password)
        print('Running remove export command')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/file remove "{}"'.format(export_name))
        print("Closing connection")    
        ssh.close()
        print("Backup for {} complete.".format(router_name))
        config_status = "Config Completed"
    except TimeoutError as err:
        print(err)
        config_status = err
    except paramiko.ssh_exception.SSHException as err:
        print(err)
        config_status = err
    except EOFError as err:
        print(err)
        config_status = err
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
        config_status = err
    except FileNotFoundError as err:
        print(err)
        config_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))
        config_status = the_value


    todays_date = datetime.datetime.today().strftime('%m-%d-%Y')
    database.update(router_name,router_ip,username,password,router_name,backup_status,config_status,todays_date)

def get_info(router_name, router_ip, username, password):
    print("Generating info for {}...".format(router_name))
    # sshing into router to create .backup and export config file
    ssh = paramiko.SSHClient()
    print('Created client')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Set ssh key')
    print('Connecting to router...')
    ssh.connect(router_ip, username=username, password=password)
    print('Running system info command')
    stdin, stdout, stderr = ssh.exec_command("/system resource print")
    system_info = stdout.read().decode('ascii').strip("\n")
    print(system_info)
    print("Closing connection")
    ssh.close()

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
        backup_status = create_backup(item['router_name'], item['router_ip'], item['username'], item['password'])
        create_config(item['router_name'], item['router_ip'], item['username'], item['password'], backup_status)

if __name__ == "__main__":
    run()