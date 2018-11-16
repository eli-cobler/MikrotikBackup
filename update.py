
def db(name, router_ip, username, password):
    # reference 
    # name of location:router_ip:routeros:username:password:enable_password
    # SPARK Office:10.10.12.1:routeros:admin:SuperSpark1@3:enable_password
    # /home/oxidized/.config/oxidized/router.db
    with open("/Users/coblere/Documents/GitHub/MikrotikBackup/router.db", 'a') as f: 
        f.write("{}:{}:routeros:{}:{}:enable_password\n".format(name, router_ip, username, password))

if __name__ == "__main__":
    name = "Test"
    router_ip = "192.168.1.1"
    username = "admin"
    password = "Admin1@3"

    db(name, router_ip, username, password)    