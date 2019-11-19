import datetime
import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase


class Router(SqlAlchemyBase):
    __tablename__ = 'routers'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    router_name = sa.Column(sa.String, index=True)
    router_ip = sa.Column(sa.String, index=True)
    username = sa.Column(sa.String)
    password = sa.Column(sa.String, index=True)

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    last_attempted = sa.Column(sa.String)

    backup_status = sa.Column(sa.String, index=True)
    config_status = sa.Column(sa.String, index=True)

    router_os_version = sa.Column(sa.String, index=True)
    uptime = sa.Column(sa.String)
    free_memory = sa.Column(sa.String)
    total_memory = sa.Column(sa.String)
    cpu_load = sa.Column(sa.String)
    free_hdd_space = sa.Column(sa.String)
    total_hdd_space = sa.Column(sa.String)
    bad_blocks = sa.Column(sa.String, index=True)
    board_name = sa.Column(sa.String, index=True)

    def __repr__(self):
        return '<Router {}>'.format(self.id)
