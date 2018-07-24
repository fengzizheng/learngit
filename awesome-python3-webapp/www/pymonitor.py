import os,time,sys,subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
'''
创建监视修改启动程序
'''

def log(s):
    print('[monitor] %s'%s)


command =['echo','ok'] #重启操作文件的信息
process=None

#退出程序
def kill_process():
    global process
    if process:
        log('kill process [%s]'%process.pid)
        process.kill()
        process.wait()
        log('process ended with code %s'%process.returncode)
        process=None

#开始程序
def start_process():
    global process,command
    log('start process %s...'%' '.join(command))
    process=subprocess.Popen(command,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)

#重启程序
def restart_process():
    kill_process()
    start_process()


#编辑MyFileSystemEventHander
class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self,fn):
        super(MyFileSystemEventHander,self).__init__()
        self.restart=fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('python source file changed:%s'%event.src_path)
            self.restart()

#监视
def start_watch(path,collback):
    observer=Observer()
    observer.schedule(MyFileSystemEventHander(restart_process),path,recursive=True)
    observer.start()
    log('watching directory %s...'%path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__=='__main__':
    argv=sys.argv[1:]
    if not argv:
        print('usage:./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0,'python')
    command=argv #操作文件的名字及程序名
    path=os.path.abspath('.')
    start_watch(path,None)