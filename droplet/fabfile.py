from __future__ import with_statement
from fabric.api import *
from fabric.operations import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

env.hosts = ['172.168.2.118']
env.user = 'root'
env.password = '123456'

def setup_web():
    hostname = run('hostname')
    run('apt-get install -y debconf-utils')
    run("debconf-set-selections <<< 'postfix postfix/main_mailer_type select Local only'")
    run("debconf-set-selections <<< 'postfix postfix/mailname string " + hostname + "'")
    run('apt-get install -y mailutils')
