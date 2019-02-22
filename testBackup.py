import datetime, paramiko, subprocess, database, os, schedule, time, backup
from datetime import date

router_name = input("What is the router_name? ")
router_ip = input("What is the router_ip? ")
username = input("What is the username? ")
password = input("What is the password? ")
backup.create(router_name, router_ip, username, password)