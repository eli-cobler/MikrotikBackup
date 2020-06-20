from typing import Optional

from MikrotikBackup.services import user_service, router_service
from MikrotikBackup.viewmodels.shared.viewmodelbase import ViewModelBase


class AddViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)
        self.router_name = self.request_dict.name
        self.router_ip = self.request_dict.router_ip
        self.username = self.request_dict.username
        self.password = self.request_dict.password
        self.ignore: Optional[str] = None

    def validate(self):
        if not self.router_name or not self.router_name.strip():
            self.error = 'You must specify a router name.'
        elif not self.router_ip or not self.router_ip.strip():
            self.error = 'You must specify a IP or Hostname.'
        elif not self.username:
            self.error = 'You must specify a username.'
        elif not self.password:
            self.error = 'You must specify a password.'
        elif router_service.find_router_by_name(self.router_name):
            self.error = 'A router with that name already exists.'