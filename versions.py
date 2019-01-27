#
#  versions.py
#  MikrotikBakcup
#
#  Created by Eli Cobler on 01/27/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  This project allows you to add and remove routers to your Oxidized Router database file.
#
#  This file allows you to track changes made to the backups folder. 

import os
import datetime
from datetime import date
def modification_date(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)

d = modification_date('/Users/coblere/Documents/GitHub/MikrotikBackup/backups/Boulevard Church/12-26-2018_19:03:16.backup')

print(d)
print(date.today())