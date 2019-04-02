import subprocess, datetime, paramiko

router_name = "Boulevard"
username = 'admin'
password = 'Admin1@3'
router_ip = '66.76.252.34'
date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
export_name = date + ".rsc"
#print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
#subprocess.run('ssh {}@{} export terse > {}'.format(username, router_ip, export_name), shell=True)

print("Generating Config for {}...".format(router_name))
# sshing into router to create .backup and export config file
ssh = paramiko.SSHClient()
print('Created client')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Set ssh key')
print('Connecting to router...')
ssh.connect(router_ip, username=username, password=password)
print('Running export command')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("export > {}".format(date))
print("Closing connection")
ssh.close()

# ssh {}@{} export terse > {}.format(username, router_ip, export_name) 

