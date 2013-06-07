#coding:utf-8

from fabric.api import run, roles, cd, parallel, task
from fabric.state import env

www_path = '/home/the5fire/selfblog'
supervisord_bin_path = '/home/the5fire/bin'
supervisord_conf_file = '/home/the5fire/conf/supervisord.conf'

env.roledefs = {
    'server': ['root@xxx.xxx.xxx']
}


@task
@roles('server')
def host_type():
    run('uname -s')


@task
@parallel(22)
@roles('server')
def top():
    run("top -b | head -n 1")


def git_co(path, branch='master'):
    with(cd(path)):
        run('git reset --hard && git pull -f && git checkout %s' % branch)


def supervisord_restart(path, conf_path):
    with(cd(path)):
        run('./supervisorctl -c %s restart all' % (conf_path, ))


@task
@roles('server')
def re_deploy(branch='django15'):
    git_co(www_path, branch=branch)
    supervisord_restart(supervisord_bin_path, supervisord_conf_file)


@task
@roles('server')
def re_mem():
    run("ps aux|grep 'the5fire/memcached' | grep -v 'grep' | awk '{print $2}' | xargs kill -9")
    run("memcached -d -m memory -s /home/the5fire/memcached.sock -P /home/the5fire/memcached.pid")
