import subprocess, datetime, database, sys

def config(router_name, username, router_ip):
    try:
        date = datetime.datetime.today().strftime('%m-%d-%Y_%H:%M:%S')
        export_name = date + ".rsc"
        #print('ssh {}@{} export terse > {}'.format(username, router_ip, export_name))
        subprocess.run('ssh {}@{} export terse > "backups/{}/{}"'.format(username, router_ip, router_name, export_name), shell=True)
    except TimeoutError as err:
        print(err)
        config_status = err
    except EOFError as err:
        print(err)
        config_status = err
    except FileNotFoundError as err:
        print(err)
        config_status = err
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print("{}\n{}".format(the_type, the_value))
        config_status = the_value

def run():
    router_list = database.get()
    routers = []
    for item in router_list:
        data = item.split(':')
        data[0] = {'router_name': data[0], 'router_ip': data[1], 'username': data[2], 'password': data[3].replace('\n', '')}
        routers.append(data[0])            
    
    for item in routers:
        print("Attempting {}...".format(item['router_name']))
        config(item['router_name'], item['username'], item['router_ip'])
        print("Finished {}...".format(item['router_name']))

if __name__ == "__main__":
    run()
