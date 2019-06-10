import database, add_file, subprocess

username = "admin"
password = "SuperSpark1@3"
router_ip = "66.76.140.245"

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])

    #for item in routers:
    #    add_file.remove_Backup_Files(item['username'], item['password'], item['router_ip'])

add_file.remove_Backup_Files(username, password, router_ip)
subprocess.run('ssh {}@{} /system script run removeBackupFiles'.format(username, router_ip), shell=True)