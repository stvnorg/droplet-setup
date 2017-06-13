from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

# Please set the env.hosts according to the real IP of WEB Server
<<<<<<< HEAD
env.hosts = ['172.168.2.116']
env.user = 'root'
env.password = 'single-electron-trunk'
=======
env.hosts = ['172.168.2.115']
env.user = 'root'
env.password = '123456'
>>>>>>> 18th Commit


def setup_web():

    if not confirm("Are you sure host " + env.hosts[0] + " is a WEB Server?"):
        abort("Abort!")

    run('apt-get update')
    run('apt-get install -y php5')    
    run('apt-get remove -y apache2')
    run('apt-get install -y nginx')
    run('apt-get install -y php5-curl php5-gd php5-mysql php5-fpm zip')
    run('apt-get install -y debconf-utils')

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
    
<<<<<<< HEAD
=======
    if not exists('/etc/nginx/nginx.conf.bak'):
        run('cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak')
    run("sed -i '70 a \\\tclient_max_body_size 5M;' /etc/nginx/nginx.conf")
>>>>>>> 18th Commit
    run('service php5-fpm restart')
    run('service nginx restart')
    run('timedatectl set-timezone Asia/Jakarta')
    hostname = run('hostname')
    run("debconf-set-selections <<< 'postfix postfix/main_mailer_type select Local only'")
    run("debconf-set-selections <<< 'postfix postfix/mailname string " + hostname + "'")
    run('apt-get install -y mailutils')
    run('apt-get install -y heirloom-mailx')
