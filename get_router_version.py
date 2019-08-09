#
#  get_router_version
#  Mikrotik Backup
#
#  Created by Eli Cobler on 08/08/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  Gets the current version of router OS running on the router. 

import subprocess, database, os, logging, paramiko

# log setup
logging.basicConfig(filename='logs/get_router_version.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.DEBUG)

def get_info(router_name,router_ip, username):
    print("Gathering info for {}...".format(router_name))
    # sshing into router to get router OS verison
    print('Running system info command')
    router_info = subprocess.run('ssh {}@{} /system resource print'.format(username, 
                                                                    router_ip),
                                                                    shell=True,
                                                                    universal_newlines=True,
                                                                    stdout=subprocess.PIPE,
                                                                    stderr=subprocess.PIPE)
    #system_info = stdout.read().decode('ascii').strip("\n")
    print(router_info.stdout)

'''def get_info(router_name,router_ip,username):
    k = paramiko.RSAKey.from_private_key_file("id_rsa-2.pub")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect( hostname = router_ip, username = username, key_filename = k )
    print("connected")
    command = [ "/system resource print"]
    print("Executing {}".format( command ))
    stdin , stdout, stderr = c.exec_command(command)
    print(stdout.read())
    print( "Errors")
    print(stderr.read())
    c.close()'''

if __name__ == "__main__":
    router_name = input("Router Name: ")
    router_ip = input("Router IP: ")
    username = input("Username: ")
    get_info(router_name, router_ip, username)


'''
import paramiko
k = paramiko.RSAKey.from_private_key_file("id_rsa-2.pub")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print "connecting"
c.connect( hostname = "www.acme.com", username = "ubuntu", pkey = k )
print "connected"
commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
for command in commands:
	print "Executing {}".format( command )
	stdin , stdout, stderr = c.exec_command(command)
	print stdout.read()
	print( "Errors")
	print stderr.read()
c.close()'''