import subprocess, datetime

username = 'admin'
password = 'Admin1@3'
router_ip = '66.76.254.96'
date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
export_name = date + ".rsc"
#print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
subprocess.run('ssh {}@{} export terse > backups/{}'.format(username, router_ip, export_name), shell=True)

# ssh {}@{} export terse > {}.format(username, router_ip, export_name) 

# ssh {}@{} export terse > {}.format(username, router_ip, export_name) 

