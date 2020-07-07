from MikrotikBackup.services import user_service
from MikrotikBackup.viewmodels.shared.viewmodelbase import ViewModelBase


class UserManagementViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)
        self.users = user_service.get_users_list()
        self.name = self.request_dict.name
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()
        self.user_to_remove = self.request_dict.user_to_remove

    def validate(self):
        if not self.name or not self.name.strip():
            self.error = 'You must specify a name.'
        elif not self.email or not self.email.strip():
            self.error = 'You must specify a email.'
        elif not self.password:
            self.error = 'You must specify a password.'
        elif len(self.password.strip()) < 10:
            self.error = 'The password must be at least 10 characters.'
        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email address already exists.'