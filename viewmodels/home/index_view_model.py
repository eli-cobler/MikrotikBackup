from services import user_service, router_service
from viewmodels.shared.viewmodelbase import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)
        self.routers = router_service.get_router_list()
        self.router_count = router_service.get_router_count()
        self.backup_complete_count = router_service.get_backup_complete_count()
        self.config_complete_count = router_service.get_config_complete_count()
        self.backup_failed_count = router_service.get_backup_failed_count()
        self.config_failed_count = router_service.get_config_failed_count()
        self.unknown_count = router_service.get_unknown_status_count()
        self.ignore_count = router_service.get_router_ignore_count()