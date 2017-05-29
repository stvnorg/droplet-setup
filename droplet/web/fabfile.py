from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
import os

env.hosts = ['172.168.2.116']
env.user = 'root'
env.password = '123456'

def install():
    run('apt-get install -y php5')    
    run('apt-get remove -y apache2')
    run('apt-get install -y nginx')
    run('apt-get install -y php5-curl php5-gd php5-mysql php5-fpm zip')
    local_path = os.getcwd() + '/000-default.conf'
    remote_path = '/etc/apache2/sites-available/000-default.conf'
    with settings(warn_only=True):
        result = put(local_path, remote_path, mode=0755)
    if result.failed and not confirm("Apache setup failed. Continue anyway?"):
        abort("Aborting at user request.")
    run('service apache2 restart')
