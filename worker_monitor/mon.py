import os
import time
from URQAProcess import URQAProcess

# pegasus command 
# apache2 pid file path "/var/run/apache2.pid" or command: "service apache2 status"

# PIDS_DIR_PATH change
# PIDS_DIR_PATH = os.path.abspath(os.path.dirname(__file__)) + '/pid'
PIDS_DIR_PATH = '/var/run/urqa-workers/'
print PIDS_DIR_PATH
NOTIFY_RETRY_COUNT = 10
WAIT_TIME = 10

# process state
activate = True
# retry count
retry = 0

def read_file(file_name):

    path_and_name = PIDS_DIR_PATH + file_name

    with open(path_and_name) as pid_file:
        pid = pid_file.readline()
        pid = pid.rstrip()
        data = {'fullpath': path_and_name, 'pid': pid, 'script_name': file_name}
        return data

def read_pids():

    global ps_data
    print PIDS_DIR_PATH
    pid_files = os.listdir(PIDS_DIR_PATH)
    ps_data = map(read_file, pid_files)
    print ps_data

def prepare():
    global processes
    processes = []

    for data in ps_data:
        process = URQAProcess(data)
        processes.append(process)

read_pids()
prepare()

while True:
    for process in processes:
        print process
        if process.is_alive():
            print "alive"
        else:
            process.retry()
            print "dead"
    time.sleep(WAIT_TIME)

'''
def notify_if_needed(retry):
    if retry > NOTIFY_RETRY_COUNT:
        # send email or something
        # exit processes
    return
'''
        
'''
def need_to_wait(activate):
    if activate == False:
        print "Wating..."

        notify_if_needed(retry)
    
        retry++
        
        # waiting few secs
        time.sleep(0.5)
        
        # reset PID
        get_process_info()
        
        return True
    else:
        retry = 0
        return False

def get_process_info():
    print "Get process info"

    try:
        p = psutil.Process(pid)
    except:
        p = None
    
    if p.is_running():
        activate = True
    else:
        activate = False

while True:
    if need_to_wait(activate):
        continue

    if p is None:
        activate = False
        continue
    
    is_running = p.is_running()
    if is_running:
        activate = True
        time.sleep(0.5)
    else:
        activate = False
        print "WhatTheHuck?"
        # run shell script
'''

