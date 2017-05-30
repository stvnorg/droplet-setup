from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

env.hosts = ['172.168.2.117']
env.user = 'root'
env.password = '123456'

def setup_db():
    if not confirm("Are you sure host " + env.hosts[0] + " is a DB Server?"):
        abort("Abort!")
    run('apt-get update')
    run('apt-get install -y php5')    
    run('apt-get remove -y apache2')
    run('apt-get install -y nginx')
    run('apt-get install -y php5-curl php5-gd php5-mysql php5-fpm php5-mcrypt zip')
    run('php5enmod mcrypt')
    run("debconf-set-selections <<< 'mysql-server mysql-server/root_password password root_db_pass'")
    run("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root_db_pass'")
    run('apt-get install -q -y mysql-server')
    run("echo -e 'root_db_pass\n n\n Y\n Y\n Y\n Y\n' | /usr/bin/mysql_secure_installation")
    run('mysql_install_db')

    local_php_path = os.getcwd() + '/php.ini'
    remote_php_path = '/etc/php5/fpm/php.ini'
    if not exists('/etc/php5/fpm/php.ini.bak'):
        run('cp /etc/php5/fpm/php.ini /etc/php5/fpm/php.ini.bak')
    with settings(warn_only=True):
        result = put(local_php_path, remote_php_path, mode=0644)
    if result.failed and not confirm("Nginx-PHP setup failed. Continue anyway?"):
        abort("Aborting at user request.")
    
    local_default_path = os.getcwd() + '/default'
    remote_default_path = '/etc/nginx/sites-available/default'
    if not exists('/etc/nginx/sites-available/default.bak'):
        run('cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak')
    with settings(warn_only=True):
        result = put(local_default_path, remote_default_path, mode=0644)
    if result.failed and not confirm("Nginx-PHP setup failed. Continue anyway?"):
        abort("Aborting at user request.")    
    
    #run('apt-get install phpmyadmin')
    run('service php5-fpm restart')
    run('service nginx restart')
    run('timedatectl set-timezone Asia/Jakarta')
