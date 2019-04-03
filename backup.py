import datetime, paramiko, subprocess, database, os, schedule, time, sys
from datetime import date 
# office ip 47.217.151.73
# home ip 47.217.140.46
# roberts home ip 66.76.254.137

def create_backup(router_name, router_ip, username, password):
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        backup_name = date + ".backup"
        #print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
        subprocess.run('ssh {}@{} /system backup save name={}'.format(username, router_ip, backup_name), shell=True)
        subprocess.run('scp {}@{}:/{} "backups/{}/{}"'.format(username, router_ip, backup_name, router_name, backup_name), shell=True)
    except TimeoutError as err:
        print(err)
        backup_status = err
    except EOFError as err:
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
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        export_name = date + ".rsc"
        #print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
        subprocess.run('ssh {}@{} export terse > "backups/{}/{}"'.format(username, router_ip, router_name, export_name), shell=True)
    except TimeoutError as err:
        print(err)
        config_status = err
    except EOFError as err:
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