from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

# Please set the env.hosts according to the real IP of API Server
env.hosts = ['172.168.2.115']
env.user = 'root'
env.password = '123456'

def setup_api():
    if not confirm("Are you sure host " + env.hosts[0] + " is an API Server?"):
        abort("Abort!")
    run('apt-get update')
    run('apt-get install -y php5 php5-curl php5-mysqlnd apache2 zip')
    run('a2enmod rewrite')

    if not exists('/etc/apache2/sites-available/000-default.conf.bak'):
        run('cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.bak')
    local_path = os.getcwd() + '/000-default.conf'
    remote_path = '/etc/apache2/sites-available/000-default.conf'
    with settings(warn_only=True):
        result = put(local_path, remote_path, mode=0644)
    if result.failed and not confirm("Apache setup failed. Continue anyway?"):
        abort("Aborting at user request.")

    local_404_path = os.getcwd() + '/404.html'
    local_50x_path = os.getcwd() + '/50x.html'
    remote_error_msg_path = '/var/www/html/'
    with settings(warn_only=True):
        result = put(local_404_path, remote_error_msg_path, mode=0644)
        result = put(local_50x_path, remote_error_msg_path, mode=0644)
    if result.failed and not confirm("Apache setup failed. Continue anyway?"):
        abort("Aborting at user request.")

    run('service apache2 restart')
    run('timedatectl set-timezone Asia/Jakarta')
