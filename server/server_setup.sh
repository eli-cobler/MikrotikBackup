#!/usr/bin/env bash

# Consider running these two commands separately
# Do a reboot before continuing.
sudo apt update
sudo apt upgrade -y

#apt install zsh
#sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Install some OS dependencies:
sudo apt-get install -y -q build-essential git unzip zip nload tree wheel
sudo apt-get install -y -q python3-pip python3-dev python3-venv
sudo apt-get install -y -q nginx
# for gzip support in uwsgi
sudo apt-get install --no-install-recommends -y -q libpcre3-dev libz-dev

# Stop the hackers
sudo apt install fail2ban -y

# Only enable this if want a firewall on the server on top of whatever firewall you are already using
#sudo ufw allow 22
#sudo ufw allow 80
#sudo ufw allow 443
## for Webmin Access
#sudo ufw allow 10000
#sudo ufw enable

# Basic git setup
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=720000'

# Be sure to put your info here:
git config --global user.email "ecobler11@gmail.com"
git config --global user.name "eli-cobler"

# Web app file structure
sudo mkdir /apps
sudo chmod 777 /apps
sudo mkdir /apps/logs
sudo mkdir /apps/logs/MikrotikBackup
sudo mkdir /apps/logs/MikrotikBackup/app_log
cd /apps

# Create a virtual env for the app.
cd /apps
sudo python3 -m venv venv
source /apps/venv/bin/activate
pip install --upgrade pip setuptools
pip install --upgrade httpie glances
pip install --upgrade uwsgi


# clone the repo:
cd /apps
sudo git clone https://github.com/eli-cobler/MikrotikBackup.git app_repo

# Setup the web app:
cd /apps/app_repo/
pip install -r requirements.txt

# Copy and enable the daemon
sudo cp /apps/app_repo/server/MikrotikBackup.service /etc/systemd/system/MikrotikBackup.service

sudo systemctl start MikrotikBackup
#sudo systemctl status ping_dashboard
sudo systemctl enable MikrotikBackup

# Setup the public facing server (NGINX)
sudo apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
sudo rm /etc/nginx/sites-enabled/default

sudo cp /apps/app_repo/server/MikrotikBackup.nginx /etc/nginx/sites-enabled/MikrotikBackup.nginx
sudo update-rc.d nginx enable
sudo service nginx restart

# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

#add-apt-repository ppa:certbot/certbot
#apt install python-certbot-nginx
#certbot --nginx -d fakepypi.talkpython.com
