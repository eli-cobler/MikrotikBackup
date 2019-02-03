import database, autoUpdate

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])

    for item in routers:
        autoUpdate.add(item['router_ip'], item['username'], item['password'])

if __name__ == "__main__":
    run()