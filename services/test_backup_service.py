from services import router_details_service
from services import backup_service

router_name = input("What is the router_name? ")
router_ip = input("What is the router_ip? ")
username = input("What is the username? ")
password = input("What is the password? ")

def run():
    backup_service.create_backup(router_name, router_ip, username)
    backup_service.create_config(router_name, router_ip, username)
    router_details_service.get_info(router_name, router_ip, username)
    router_details_service.parse_info(router_name)

if __name__ == "__main__":
    run()