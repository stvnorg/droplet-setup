from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm

env.hosts = ['172.168.2.115']
env.user = 'root'
env.password = '123456'


def hello(name):
    print ("Hello " + name + "!")

def install():
    run('uname -a')
    run('apt-get install -y php5 php5-curl php5-mysqlnd apache2 zip')    
    run('a2enmod rewrite')
    run('service apache2 restart')
    with settings(warn_only=True):
        result = run('cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.bak')
    if result.failed and not confirm("Apache setup failed. Continue anyway?"):
        abort("Aborting at user request.")
