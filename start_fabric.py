#!/bin/env python
#coding=utf-8
from fabric.api import *
from datetime import datetime

env.hosts = ['192.168.213.248','192.168.213.249']
env.password = 'root'
env.warn_only = True
#env.gateway = '192.168.213.241' 跳转机环境
env.path = '/opt/trx_init'+ datetime.now().strftime("%Y%m%d_%H")
env.sh = '/opt/init.sh'
env.config = '/opt/config'
env.py = '/opt/python-3.5.6.tar.gz'
env.pydir = 'Python-3.5.6'
env.uuid = '/opt/access.uuid'
env.center = '/opt/count.center'

def remote_task1():
      run('mkdir %s' %(env.path))
      with cd('%s' %(env.path)):
        put('%s' %(env.sh),'init.sh')
        put('%s' %(env.config),'config')
        run('bash init.sh')
        
def remote_task2():
      with cd('%s' %(env.path)):
        put('%s' %(env.py),'python-3.5.6.tar.gz')
        run('tar -xvzf python-3.5.6.tar.gz')
        with cd('%s' %(env.pydir)):
          run('./configure;make;make install')
          run('mv /usr/bin/python /usr/bin/pythonold')
          run('ln -s /usr/local/bin/python3 /usr/bin/python')
          run('sed -i 1s/python/pythonold/ /usr/bin/yum')
          run('sed -i 1s/python/pythonold/ /usr/libexec/urlgrabber-ext-down')

@runs_once
#临时任务，限定在第一台机器执行
def remote_task3():
      with cd('%s' %(env.path)):
        run('mkdir test-Department')
        with cd('test-Department'):
          put('%s' %(env.uuid),'uuid')
        run('mkdir development-Department')
        with cd('development-Department'):
          put('%s' %(env.center),'center')


def restart():
      reboot()

execute(remote_task1)
execute(remote_task2)
#execute(remote_task3)  
execute(restart)
