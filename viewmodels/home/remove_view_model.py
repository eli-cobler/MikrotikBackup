from typing import Optional

from services import user_service, router_service
from viewmodels.shared.viewmodelbase import ViewModelBase


class RemoveViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)
        self.routers = router_service.get_router_list()
        self.router_to_remove = self.request_dict.selected_router