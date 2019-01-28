import datetime, paramiko, subprocess, database, os, schedule, time
from datetime import date 
# office ip 47.217.151.73
# home ip 47.217.140.46
# roberts home ip 66.76.254.137

def create(router_name, router_ip, username, password):
    # getting current date and time for naming backup file
    date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
    filename = date + ".backup"

    try:
        print("Generating backup for {}...".format(router_name))
        # sshing into router to create .backup file
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

        # sftping backup file from router to server
        transport = paramiko.Transport((router_ip))
        print("Transport created")
        print("Attemption connection...")
        transport.connect(username = username, password = password)
        print("Sftp created")
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Set remote and local path")
        remotepath = "/{}.backup".format(date)
        localpath = 'backups/{}/{}'.format(router_name,filename)
        print("Backup transfered")
        sftp.get(remotepath, localpath)
        print("Closing sftp and transport")
        sftp.close()
        transport.close()

        # sshing back into router to remove .backup file
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
        status = "Backup Completed"
    except TimeoutError as err:
        print(err)
        status = err
    except paramiko.ssh_exception.SSHException as err:
        print(err)
        status = err
    except EOFError as err:
        print(err)
        status = err
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err)
        status = err
    except:
        print("Unexpected Error, no backup was grabbed.")
        status = "Unexpected Error"

    todays_date = datetime.datetime.date.today().strftime('%m-%d-%Y')
    database.update(router_name,router_ip,username,password,router_name,status, todays_date)

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
        create(item['router_name'], item['router_ip'], item['username'], item['password'])

if __name__ == "__main__":
    run()