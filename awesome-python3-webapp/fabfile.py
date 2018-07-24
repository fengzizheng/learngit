import os,re
from datetime import datetime
from fabric.api import *

env.user='test'
env.sudo_user='root'
env.hosts=['192.168.17.129']
db_user='www-data'
db_password='www-data'

_TAR_FILE='dist-awesome.tar.gz'
_REMOTE_TMP_TAR ='tmp/%s'% _TAR_FILE
_REMOTE_BASE_DIR ='/srv/awesome'

def _current_path():
    return os.path.abspath('.')

def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')


def backup():
    '''
    dump entire database on server and backup to local
    :return:
    '''
    dt= _now()
    f='backup-awesome-%s.sql'%dt
    with cd('/tmp'):
        run('msqldump --user=%s --password=%s --skip-opt --add-drop-table -default-character-set=utf8 --quick awesome>% s'%(
            db_user,db_password,f ))
        run('tar -czvf %s.tar.gz %s'%(f,f))
        get('%s.tar.gz'%f,'%s/backup/'%_current_path())
        run('rm -f %s'%f)
        run('rm -f %s.tar.gz'%f)

def build():
    '''
    build dist package
    :return:
    '''
    includes=['static','templates','transwrap','favicon.ico','*.py']
    excludes=['test','.*','*.pyc','*.pyo']
    local('rm -f dist/%s'%_TAR_FILE)
    with lcd(os.path.join(_current_path(),'www')):
        cmd=['tar','--dereference','-czvf','../dist/%s'% _TAR_FILE]
        cmd.extend(['--exclude=\'%s\''%ex for ex in includes])
        cmd.extend(includes)
        local(' '.join(cmd))




def deploy():
    newdir='www-%s'%_now()
    run('rm -f %s'% _REMOTE_TMP_TAR)
    put('dist/%s'% _TAR_FILE,_REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s'%newdir)
    with cd('%s %s'%(_REMOTE_BASE_DIR,newdir)):
        sudo('tar -xzvf %s'%_REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ls -s %s www' %newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s'%newdir)
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx reload')


RE_FILES=re.compile('\r?\n')

def rollback():
    with cd(_REMOTE_BASE_DIR):
        r=run('ls -p -1')
        files=[s[:-1]for s in RE_FILES.split(r) if s.startswith('www-') and s.endswith('/')]
        files.sort(cmp=lambda s1,s2: 1 if s1<s2 else -1)
        r=run('ls -l www')
        ss=r.split('->')
        if len(ss)!=2:
            print('ERROR:\WWW\'is not a symbol link')
            return
        current=ss[1]
        print('found current symbol link points to:%s \n'%current)
        try:
            index=files.index(current)
        except ValueError as e:
            print('Error:symbol link is invalid')
            return
        if len(files)==index+1:
            print('error:already the oldest version')
        old=files[index+1]
        print('===============================================')
        for f in files:
            if f==current:
                print('current --->%s'%current)
            elif f==old:
                print('rollback to --->'%old)
            else:
                print('%s'%f)
        print('=====================================')
        print('')
        yn=input('continue? y/n')
        if yn !='y'and yn !='Y':
            print('rollback cancelled')
            return
        print('start rollback')
        sudo('rm -f www')
        sudo('ln -s %s www'%old)
        sudo('chown www-data:www-data www')
        with settings(warn_only=True):
            sudo('supervisorctl stop awesome')
            sudo('supervisorctl start awesome')
            sudo('/etc/init.d/nginx reload')
        print('rollback ok')

