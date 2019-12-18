import shutil, os
from tqdm import tqdm
from data import db_session
from services import router_service

def main():
    init_db()
    run()

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..','db','mikrotikbackup.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

def run():
    routers = router_service.get_router_list()
    ignore_list = router_service.get_router_ignore_list()

    router_count = 0
    for r in routers:
        router_count += 1

    for router in tqdm(routers, total=router_count, unit=" router"):
        top_folder = os.path.dirname(__file__)
        rel_file = os.path.join('..', 'backups', router.router_name)
        backup_path = os.path.abspath(os.path.join(top_folder, rel_file))
        zip_path = os.path.join(backup_path,f'{router.router_name}.zip')

        if router.router_name in ignore_list:
            tqdm.write(f'{router.router_name} skipped.')
        elif os.path.exists(zip_path):
            tqdm.write(f'{router.router_name} Found.')
            tqdm.write(f'Removing old {router.router_name}.zip')
            os.remove(zip_path)
            tqdm.write(f'{router.router_name} removed.')
            tqdm.write(f'Creating new {router.router_name}.zip')
            shutil.make_archive(router.router_name, 'zip', backup_path)
            tqdm.write(f'New {router.router_name}.zip created.')
            tqdm.write(f'Moving {router.router_name}.zip to backup directory.')
            os.rename(f'{router.router_name}.zip', f'{backup_path}/{router.router_name}.zip')
            tqdm.write(f'{router.router_name}.zip moved.')
        else:
            tqdm.write(f'{router.router_name} Not Found.')
            tqdm.write(f'Creating new {router.router_name}.zip')
            shutil.make_archive(router.router_name,'zip',backup_path)
            tqdm.write(f'New {router.router_name}.zip created.')
            tqdm.write(f'Moving {router.router_name}.zip to backup directory.')
            os.rename(f'{router.router_name}.zip', f'{backup_path}/{router.router_name}.zip')
            tqdm.write(f'{router.router_name}.zip moved.')

if __name__ == '__main__':
    main()