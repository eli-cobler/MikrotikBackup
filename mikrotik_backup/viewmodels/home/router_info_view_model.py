from mikrotik_backup.services import user_service, router_service
from mikrotik_backup.viewmodels.shared.viewmodelbase import ViewModelBase


class RouterInfoViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)
        self.router_name = self.request.path.strip('/router-info/')
        self.router = router_service.get_router_details(self.request.path.strip('/router-info/'))
        self.uptime = self.router.uptime
        self.version = self.router.router_os_version
        self.free_memory = self.router.free_memory
        self.total_memory = self.router.total_memory
        self.cpu_load = self.router.cpu_load
        self.free_hdd_space = self.router.free_hdd_space
        self.total_hdd_space = self.router.total_hdd_space
        self.bad_blocks = self.router.bad_blocks
        self.board_name = self.router.board_name