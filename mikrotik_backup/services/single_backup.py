import sys, os
current_directory = os.getcwd()
sys.path.insert(1,current_directory.replace('/mikrotik_backup',''))
import mikrotik_backup.services.backup as backup

def run(router_name, router_ip, username, password):
    backup_status = backup.create_backup(router_name, router_ip, username, password)
    backup.create_config(router_name, router_ip, username, password, backup_status)
