from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

# Please set the env.hosts according to the real IP of DB Server
env.hosts = ['172.168.2.117']
env.user = 'root'
env.password = '123456'

API_SERVER_IP = '172.168.2.115'
WEB_SERVER_IP = '172.168.2.116'
DB_SERVER_IP = '172.168.2.117'

MYSQL_LOGIN = "mysql -uroot -proot_db_pass -e "

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
    run(MYSQL_LOGIN + "\"GRANT ALL PRIVILEGES ON *.* TO 'root'@'" + API_SERVER_IP + "' IDENTIFIED BY 'root_db_pass' WITH GRANT OPTION;\"")
    run(MYSQL_LOGIN + "\"GRANT ALL PRIVILEGES ON *.* TO 'root'@'" + WEB_SERVER_IP + "' IDENTIFIED BY 'root_db_pass' WITH GRANT OPTION;\"")
    run(MYSQL_LOGIN + "\"GRANT ALL PRIVILEGES ON *.* TO 'root_dev'@'localhost' IDENTIFIED BY 'root_dev_pass' WITH GRANT OPTION;\"")
    run(MYSQL_LOGIN + "\"GRANT ALL PRIVILEGES ON *.* TO 'root_dev'@'%' IDENTIFIED BY 'root_dev_pass' WITH GRANT OPTION;\"")
    run(MYSQL_LOGIN + "\"FLUSH PRIVILEGES;\"")

    if not exists('/etc/mysql/my.cnf.bak'):
        run('cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak')
    run("sed -e 's/127.0.0.1/" + DB_SERVER_IP + "/g' /etc/mysql/my.cnf.bak > /etc/mysql/my.cnf")
    run('service mysql restart')

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
    
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/app-password-confirm root_db_pass'")
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/password-confirm root_db_pass'")    
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/mysql/app-pass root_db_pass'")
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/mysql/admin-pass root_db_pass'")
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/setup-password root_db_pass'")
    run("debconf-set-selections <<< 'phpmyadmin phpmyadmin/dbconfig-install true'")
    run('apt-get install -y phpmyadmin')
    run('ln -s /usr/share/phpmyadmin /usr/share/nginx/html')
    run('service php5-fpm restart')
    run('service mysql restart')
    run('service nginx restart')
    run('timedatectl set-timezone Asia/Jakarta')
