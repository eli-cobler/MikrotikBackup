
def db(name, router_ip, username, password):
    # Used for reference 
    # name of location:router_ip:routeros:username:password:enable_password
    # SPARK Office:10.10.12.1:routeros:admin:SuperSpark1@3:enable_password
    # /home/oxidized/.config/oxidized/router.db
    with open("/home/oxidized/.config/oxidized/router.db", 'a') as f: 
        f.write("{}:{}:routeros:{}:{}:enable_password\n".format(name, router_ip, username, password))  # writes new router to database file   