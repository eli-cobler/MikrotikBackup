import subprocess, datetime, database

def config(router_name, username, router_ip):
    date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
    export_name = date + ".rsc"
    #print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
    subprocess.run('ssh {}@{} export terse > backups/{}/{}'.format(username, router_ip, router_name, export_name), shell=True)

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
         config(item['router_name'], item['username'], item['router_ip'])

if __name__ == "__main__":
    run()
