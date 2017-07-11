#!/usr/bin/python
# -*- encoding: utf-8 -*-
#****************************************************************#
# ScriptName: /srv/salt/_modules/autopublishing.py
# Create Date: 2014-08-07 09:30
# Modify Date: 2014-08-07 09:30
#***************************************************************#

import os
import re
import sys
import pwd
import json
import stat
import time
import urllib
import tempfile
import hashlib
import requests
import logging
import httplib
import urllib
import urlparse
import subprocess
import signal
import socket
import shutil
import traceback
import subprocess
from threading import Timer
# from urllib import request


API_HOST = 'cmdb.xxd.com'
API_URL = 'http://172.16.18.149:8005/api/release'
TMP_DIR = '/tmp'
LOGGER_FILE = '/home/admin/logs/autopublishing.log'
RUNNING_USER = 'admin'
HOME_DIR = '/home/admin'
LOGGER = None
AUTH_KEY = 'vLCzbZjGVNKWPxqd'
CMDB_WORKSPACE = '/root/.cmdb/workspace/'
run_log_file = '/home/admin/logs/run.log'
error_log_file = '/home/admin/logs/err.log'
CHECK_SERVICE_TIMEOUT = 60

# define return code
RET_OK = 0
ERROR = 1
RET_FINISHED = 10000
RET_ERROR_DOWNLOAD_FILE_FAILED = 10001
RET_ERROR_CHECK_FILE_MD5SUM_FAILED = 10002
RET_ERROR_STOP_SERVICE_FAILED = 10003
RET_ERROR_CLEAN_ORIGINAL_FILE_FAILED = 10004
RET_ERROR_PUBLISH_FILE_FAILED = 10005
RET_ERROR_START_SERVICE_FAILED = 10006
RET_ERROR_CHECK_SERVICE_FAILED = 10007
RET_ERROR_UNKNOW_FILE_TYPE = 10008
RET_ERROR_RUN_EXCEPTION = 10009


class Logger(object):
    __instance = None

    def __init__(self):
        self.run_log_file = run_log_file
        self.error_log_file = error_log_file
        self.run_logger = None
        self.error_logger = None

        self.initialize_run_log()
        self.initialize_error_log()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def check_path_exist(log_abs_file):
        log_path = os.path.split(log_abs_file)[0]
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    def initialize_run_log(self):
        # self.check_path_exist(self.run_log_file)
        file_1_1 = logging.FileHandler(self.run_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.INFO)
        logger1.addHandler(file_1_1)
        self.run_logger = logger1

    def initialize_error_log(self):
        # self.check_path_exist(self.error_log_file)
        file_1_1 = logging.FileHandler(self.error_log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s  - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.ERROR)
        logger1.addHandler(file_1_1)
        self.error_logger = logger1

    def log(self, message, mode=True):
        """
        写入日志
        :param message: 日志信息
        :param mode: True表示运行信息，False表示错误信息
        :return:
        """
        if mode:
            self.run_logger.info(message)
        else:
            self.error_logger.error(message)
# stage info
STAGE_MESSAGE_INFO = {
    'gitPullCode': {
        'success': {
            'dbMessage': '拉取代码成功;',
            'logMessage': 'pull code......success'
        },
        'failure': {
            'dbMessage': '拉取代码失败;',
            'logMessage': 'pull code......failure'
        }
    },
    'downloadFile': {
        'success': {
            'dbMessage': '下载发布文件成功;',    
            'logMessage': 'download file......success'
        },
        'failure': {
            'dbMessage': '下载发布文件失败;',    
            'logMessage': 'download file......failure'
        }
    },    
    'checkMd5sum': {
        'success': {
            'dbMessage': '发布文件校验正确;',    
            'logMessage': 'check file md5sum......success'
        },
        'failure': {
            'dbMessage': '发布文件校验错误;',    
            'logMessage': 'check file md5sum......failure'
        }
    },    
    'stopTengineService': {
        'success': {
            'dbMessage': '停止nginx服务成功;',
            'logMessage': 'stop nginx service......success'
        },
        'failure': {
            'dbMessage': '停止服务失败;', 
            'logMessage': 'stop nginx service......failure'
            }
    },
    'stopService': {
        'success': {
            'dbMessage': '停止服务成功;',    
            'logMessage': 'stop service......success'
        },
        'failure': {
            'dbMessage': '停止服务失败;',    
            'logMessage': 'stop service......failure'
        }
    },        
    'cleanOldFiles': {
        'success': {
            'dbMessage': '清除原文件成功;',    
            'logMessage': 'clean old files......success'
        },
        'failure': {
            'dbMessage': '清除原文件失败;',    
            'logMessage': 'clean old files......failure'
        }
    },        
    'publishFiles': {
        'success': {
            'dbMessage': '部署文件成功;',    
            'logMessage': 'copy publish files......success'
        },
        'failure': {
            'dbMessage': '部署文件失败;',    
            'logMessage': 'copy publish files......failure'
        }
    },
    'startTengineService': {
        'success': {
            'dbMessage': '启动nginx服务成功',
            'logMessage': 'start nginx service......success'
        },
        'failure': {
            'dbMessage': '启动nginx服务失败;',
            'logMessage': 'start nginx service......failure'
        }
    },
    'startService': {
        'success': {
            'dbMessage': '启动服务成功;',    
            'logMessage': 'start service......success'
        },
        'failure': {
            'dbMessage': '启动服务失败;',    
            'logMessage': 'start service......failure'
        }
    },        
    'checkService': {
        'success': {
            'dbMessage': '检查服务成功;',    
            'logMessage': 'check service......success'
        },
        'failure': {
            'dbMessage': '检查服务失败;',    
            'logMessage': 'check service......failure'
        }
    },        
}


#发布流程： 下载包文件->停止服务->清除原文件->复制新包->启动服务->检查服务

def setRunningUser(username):
    uid = pwd.getpwnam(username).pw_uid
    os.setgid(uid)
    os.setuid(uid)
    os.setreuid(uid, uid)
    os.setregid(uid, uid)

def getLocalIp():
    return socket.gethostbyname(socket.gethostname())

def execSystemCommand(cmd, timeout=30):
    """ run cmd return output and status, timeout will return"""
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    killProc = lambda pid: os.killpg(pid, signal.SIGKILL)
    timer = Timer(timeout, killProc, [popen.pid])
    timer.start()
    popen.wait()
    output = popen.stdout.read()
    timer.cancel()

    return popen.returncode, output

def execSystemCommandRunAs(cmd, user, timeout=30):
    """ run cmd return output and status, timeout will return"""
    cmd = "su - %s -c '%s'" %(user, cmd)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    killProc = lambda pid: os.killpg(pid, signal.SIGKILL)
    timer = Timer(timeout, killProc, [popen.pid])
    timer.start()
    popen.wait()
    output = popen.stdout.read()
    timer.cancel()
    Logger().log('%s->%s' % (cmd, output), True)

    return popen.returncode, output


def kill(pid):
    try:
        pid = int(pid)
        os.kill(pid, signal.SIGKILL)
    except Exception, e:
        LOGGER.info('kill %s process failed, %s' %(pid, str(e)))
        return False

    return True

def sendHttpGetRequest(server, url, params={}, port=80):
    try:
        conn = httplib.HTTPConnection(server, port, timeout=30)
        headers = {'User-Agent': 'XXD Agent'}
        url = url + urllib.urlencode(params)
        conn.request('GET', url, headers=headers)
        response = conn.getresponse()
        status = response.status
        data = response.read()
    except Exception, e:
        status = -1
        data = str(e)

    return status,data

def sendHttpPostRequest(server, url, params, port=80):
    try:
        conn = httplib.HTTPConnection(server, timeout=30)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request('POST', url, urllib.urlencode(params), headers)
        response = conn.getresponse()
        status = response.status
        data = response.read()
    except Exception, e:
        status = -1
        data = str(e)

    return status,data

def sendHttpsPostRequest(server, url, params, port=443):
    try:
        conn = httplib.HTTPSConnection(server, timeout=30)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request('POST', url, urllib.urlencode(params), headers)
        response = conn.getresponse()
        status = response.status
        data = response.read()
    except Exception, e:
        status = -1
        data = str(e)

    return status,data

def initLogger(logfile):
    dirname = os.path.dirname(logfile)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    logger = logging.getLogger('AUTO_PUBLISHING')
    logHandle = logging.FileHandler(logfile)
    format = '%(asctime)s - %(levelname)s - %(message)s'
    logFormatter = logging.Formatter(format)
    logHandle.setFormatter(logFormatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logHandle)

    return logger

def moveFile(path, filename, destPath, matchPrefix=False):
    # matchPrefix表示匹配filename开头的所有文件
    for file in os.listdir(path):
        regex = '^%s' %filename
        if not matchPrefix:
            regex = '%s$' %regex
        if re.match(regex, file):
            try:
                backupPath = os.path.join(destPath, file) + '.orig'
                shutil.move(os.path.join(path, file), backupPath)
                LOGGER.debug("Clean files: %s -> %s" %(os.path.join(path, file), backupPath))
                Logger().log('Clean files: %s -> %s' %(os.path.join(path, file), backupPath))
            except Exception, e:
                LOGGER.info(str(e))
                return RET_ERROR_CLEAN_ORIGINAL_FILE_FAILED

    return RET_OK

def removeFile(path, filename, matchPrefix=False):
    # matchPrefix表示匹配filename开头的所有文件
    for file in os.listdir(path):
        regex = '^%s' %filename
        if not matchPrefix:
            regex = '%s$' %regex
        if re.match(regex, file):
            try:
                shutil.remove(os.path.join(path, file))
                Logger().log('shutil.remove: %s' % os.path.join(path, file))
            except Exception, e:
                LOGGER.info(str(e))
                return RET_ERROR_CLEAN_ORIGINAL_FILE_FAILED

    return RET_OK

def clean(path):
    os.system('rm -rf %s' %path)

def getJavaPids():
    retCode, output = execSystemCommand('jps')
    pids = set([i for i in output.split('\n') if i != '' and i.find('Jps') == -1])
    return pids

def getJavaAppPid():
    retCode, output = execSystemCommand('jps')
    for i in output.split('\n'):
        if not i:
            continue
        pid, pidName = i.split(' ')
        #该功能主要针对API应用，API的应用名字为Bootstrap
        if pidName == 'Bootstrap':
            return pid

    return None

def checkFileMd5sum(filepath, md5sum):
    with open(filepath) as f:
        data = f.read()    
        currentMd5sum = hashlib.md5(data).hexdigest()
        Logger().log('%s->%s' % (filepath, md5sum), True)

    if currentMd5sum != md5sum:
        Logger().log('MD5 check failed... %s->%s' % (filepath, md5sum), False)
        return RET_ERROR_CHECK_FILE_MD5SUM_FAILED

    return RET_OK

def downloadFile(path, dest):
    ul =urllib.URLopener()
    try:
        ul.retrieve(path, dest)
        Logger().log('%s->%s' % (path, dest), True)
    except IOError, e:
        LOGGER.info('Download file failed: %s, exception: %s' % (path, str(e)))
        Logger().log('Download file failed: %s, exception: %s' % (path, str(e)), False)
        return RET_ERROR_DOWNLOAD_FILE_FAILED

    return RET_OK

def commitTaskStatus(taskId, msg, retCode):
    params = {
        'taskId': taskId,
        'host': getLocalIp(),
        'desc': msg,
        'retCode': retCode,
        'method': 'commitTaskStatus',
    }
    

    retCode, output = sendHttpGetRequest(API_HOST, API_URL, params)

    if retCode != 200:
        LOGGER.info('%s %s' %(retCode, output))
        return False

    result = json.loads(output)
    if result.get('retCode') != 0:
        LOGGER.info('Commit task status failed, error code: %s, desc: %s' %(result.get('retCode'), 
                                                                             str(result.get('description'))))
        return False

    return True

def recordStageLog(taskId, stage, retCode, output=None):
    if output:
        LOGGER.debug('%s -> retCode: %s, output: %s' %(stage, retCode, output))
    else:
        LOGGER.debug('%s -> retCode: %s' %(stage, retCode))
    status = retCode==RET_OK and 'success' or 'failure'
    logMessage = STAGE_MESSAGE_INFO[stage][status]['logMessage']
    LOGGER.info(logMessage)

    dbMessage = STAGE_MESSAGE_INFO[stage][status]['dbMessage']
    commitTaskStatus(taskId, dbMessage, retCode)


def checkApiService(ip):
    # retCode = RET_ERROR_CHECK_SERVICE_FAILED
    cmd = 'ps -ef | grep java | wc -l'
    retCode, output = execSystemCommandRunAs(cmd, 'admin')
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    # out, err = p.communicate()
    # out = str(out, encoding='utf-8')
    if output.split()[0] == '2':
        Logger().log('check services --> Java process not start....', True)
        return RET_ERROR_CHECK_SERVICE_FAILED
    else:
        # curl 检查服务是否正常
        total_time = CHECK_SERVICE_TIMEOUT
        while total_time > 0:
            total_time -= 1
            time.sleep(1)
            cmd = "curl -I -m 2 %s:8080" % ip
            ret = os.system(cmd)
            if ret == 0:
                Logger().log('check services --> Java start success....', True)
                return 0
            else:
                Logger().log('check services --> try to start....%s' % total_time, True)
                continue
        return RET_ERROR_CHECK_SERVICE_FAILED


def publishCommonService(config, runas):
    retCode = RET_OK

    # stop service
    if os.path.exists(config['stopServiceCommand']):
        stopServiceCommand = "cd %s; bash %s stop" %(os.path.join(config['publishPath'], config['appFilePrefix']),
                                                         os.path.basename(config['stopServiceCommand']))
        retCode, output = execSystemCommandRunAs(stopServiceCommand, runas)
        recordStageLog(config['taskId'], 'stopService', retCode, output)
        if retCode != RET_OK: return retCode
    
    # clean old files
    needCleanPath = os.path.join(config['publishPath'], config['appFilePrefix'])
    if os.path.exists(needCleanPath):
        retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=False)
        recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
        if retCode != RET_OK: return retCode
    else:
        if not os.path.exists(config['publishPath']):
            os.makedirs(config['publishPath'])

    # publish files
    cmd = '/usr/bin/unzip -x %s -d %s > /dev/null' %(config['destFile'], os.path.join(config['publishPath'], config['appFilePrefix']))
    retCode, output = execSystemCommandRunAs(cmd, runas)
    recordStageLog(config['taskId'], 'publishFiles', retCode, output)
    if retCode != RET_OK: return retCode

    # start service
    startServiceCommand = "cd %s;bash %s start" %(os.path.join(config['publishPath'], config['appFilePrefix']),
                                                      os.path.basename(config['startServiceCommand']))
    retCode, output = execSystemCommandRunAs(startServiceCommand, runas, timeout=300)
    recordStageLog(config['taskId'], 'startService', retCode, output)
    if retCode != RET_OK: return retCode

    # check service
    checkServiceCommand = "cd %s;bash %s status" %(os.path.join(config['publishPath'], config['appFilePrefix']),
                                                      os.path.basename(config['startServiceCommand']))
    retCode, output = execSystemCommandRunAs(checkServiceCommand, runas, timeout=300)
    recordStageLog(config['taskId'], 'checkService', retCode, output)
    if retCode != RET_OK: return retCode

    return retCode

def publishTomcatService(config, runas):
    retCode = RET_OK

    # if config['appFilePrefix'] == 'api':
    #     retCode, output = execSystemCommandRunAs(config['stopTengineCommand'], runas)
    #     recordStageLog(config['taskId'], 'stopTengineService', retCode, output)
    #     if retCode != RET_OK: return retCode

    # stop service
    if os.path.exists(config['stopServiceCommand']):
        cmd = 'ps -ef | grep java | wc -l'
        retCode, output = execSystemCommandRunAs(cmd, runas)
        # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        # out, err = p.communicate()
        # out = str(out, encoding='utf-8')
        # Logger().log('%s --> %s....' % (cmd, out.split()[0]), True)
        out = output
        if out.split()[0] == '2':
            Logger().log('stop services --> Java process not start....', True)
        else:
            retCode, output = execSystemCommandRunAs(config['stopServiceCommand'], runas)
            Logger().log('stop service --> %s %s' % (retCode, output))
            recordStageLog(config['taskId'], 'stopService', retCode, output)
            time.sleep(3)

            # 如果java进程无法关闭 kill进程
            # p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            cmd = "ps -A"
            retCode, output = execSystemCommandRunAs(cmd, runas)
            # Logger().log('stop pid --> %s %s' % (config['stopServiceCommand'], output))

            # out, err = p.communicate()
            # s = bytes('java', encoding='utf-8')
            s = 'java'
            for line in output.splitlines():
                if s in line:
                    pid = line.split()[0]
                    os.kill(int(pid), signal.SIGKILL)
                    Logger().log('kill pid --> %s' % pid)
        # if retCode != RET_OK: return retCode

    # clean old files
    needCleanPath = os.path.join(config['publishPath'], config['appFilePrefix'])
    Logger().log('needcleanPath-->%s' % needCleanPath)
    if os.path.exists(needCleanPath):
        retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=True)
        recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
        if retCode != RET_OK: return retCode
        cmd = '/bin/rm -rf %s/ROOT' % (config['publishPath'])
        retCode, output = execSystemCommandRunAs(cmd, runas)
        cmd = '/bin/rm -rf /usr/local/tomcat/work/Catalina'
        retCode, output = execSystemCommandRunAs(cmd, runas)

    # publish files
    # cmd = '/bin/cp %s %s/%s.war' %(config['destFile'], config['publishPath'], config['appFilePrefix'])
    cmd = '/bin/cp %s %s%s' %(config['destFile'], config['publishPath'], config['appFilePrefix'])
    retCode, output = execSystemCommandRunAs(cmd, runas)
    Logger().log(cmd, True)
    recordStageLog(config['taskId'], 'publishFiles', retCode, output)
    if retCode != RET_OK: return retCode

    # start service
    retCode, output = execSystemCommandRunAs(config['startServiceCommand'], runas, timeout=300)
    recordStageLog(config['taskId'], 'startService', retCode, output)
    if retCode != RET_OK: return retCode

    if config['appFilePrefix'] == 'api':
        retCode, output = execSystemCommandRunAs(config['startTengineCommand'], runas)
        recordStageLog(config['taskId'], 'startTengineService', retCode, output)
        if retCode != RET_OK: return retCode

    # check service
    if config['appFilePrefix'] == 'api':
        retCode = checkApiService()
        recordStageLog(config['taskId'], 'checkService', retCode, '')

    retCode = checkApiService('0.0.0.0')
    if retCode != RET_OK: return retCode

    return retCode

def publishApijarService(config, runas):
    retCode = RET_OK

    # stop tengine
    if os.path.exists(config['stopTengineCommand']):
        retCode, output = execSystemCommandRunAs(config['stopTengineCommand'], runas)
        recordStageLog(config['taskId'], 'stopTengineService', retCode, output)
        if retCode != RET_OK: return retCode

    # stop service
    if os.path.exists(config['stopServiceCommand']):
        retCode, output = execSystemCommandRunAs(config['stopServiceCommand'], runas)
        recordStageLog(config['taskId'], 'stopService', retCode, output)
        if retCode != RET_OK: return retCode
    
    # clean old files
    needCleanPath = config['publishPath']
    if os.path.exists(needCleanPath):
        retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=True)
        recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
        if retCode != RET_OK: return retCode

    # publish files
    cmd = '/bin/cp %s %s' %(config['destFile'], config['publishPath'])
    retCode, output = execSystemCommandRunAs(cmd, runas)
    recordStageLog(config['taskId'], 'publishFiles', retCode, output)
    if retCode != RET_OK: return retCode

    # start service
    retCode, output = execSystemCommandRunAs(config['startServiceCommand'], runas, timeout=300)
    recordStageLog(config['taskId'], 'startService', retCode, output)
    # if retCode != RET_OK: return retCode
    time.sleep(3)

    #start tengine
    # if os.path.exists(config['startTengineCommand']):
    #     retCode, output = execSystemCommandRunAs(config['startTengineCommand'], runas)
    #     recordStageLog(config['taskId'], 'startTengineService', retCode, output)
    #     if retCode != RET_OK: return retCode

    print 5555
    # check service
    retCode = checkApiService(ip='0.0.0.0')
    recordStageLog(config['taskId'], 'checkService', retCode, '')

    return retCode

def publishHtmlService(config, runas):
    retCode = RET_OK

    if not os.path.exists(config['publishPath']):
        execSystemCommandRunAs('mkdir -p %s' %config['publishPath'], runas)

    # clean old files
    #needCleanPath = os.path.join(config['publishPath'], config['appFilePrefix'])
    #if os.path.exists(needCleanPath):
    #    retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=False)
    #    recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
    #    if retCode != RET_OK: return retCode

    # publish files
    cmd_file = '/home/admin/rsync_all.sh %s' %(config['appFilePrefix'])
    sync_file = '/home/admin/rsync_all.sh'
    cmd = "sudo /etc/init.d/tengine stop"
    retCode, output = execSystemCommandRunAs(cmd, runas, timeout=300)
    if retCode != RET_OK: return retCode

    cmd = '/usr/bin/unzip -o -x %s -d %s > /dev/null' %(config['destFile'], os.path.join(config['publishPath'], config['appFilePrefix']))
    retCode, output = execSystemCommandRunAs(cmd, runas, timeout=300)
    if retCode != RET_OK: return retCode

    cmd = "sudo /etc/init.d/tengine start"
    retCode, output = execSystemCommandRunAs(cmd, runas, timeout=300)
    if retCode != RET_OK: return retCode

    if os.path.exists(sync_file):
        retCode, output = execSystemCommandRunAs(cmd_file, runas, timeout=1800)
    else:
        retCode = RET_OK

    recordStageLog(config['taskId'], 'publishFiles', retCode, output)
    if retCode != RET_OK: return retCode


    # check service

    return retCode

def runTask(pkgUrl, md5sum, taskId, serviceType, runas):
    # build.xxd.com/infra/cmdb/97/cmdb.war 6d200fd40a846900c72574e0521b7e26 97 tomcat
    config = {}
    url = urlparse.urlparse(pkgUrl)
    filename = os.path.basename(url.path)
    fileSuffix = filename.split('.')[-1]
    config['taskId'] = taskId
    config['appFilePrefix'] = filename.split('_')[1]
    config['tempDir'] = tempfile.mkdtemp(prefix='%s-' %config['appFilePrefix'], dir='/tmp/')
    config['destFile'] = os.path.join(config['tempDir'], filename)
    os.chmod(config['tempDir'], stat.S_IRWXG+stat.S_IRWXO+stat.S_IRWXU)
    Logger().log(config, True)
    # print config

    LOGGER.info('=== start publishing ===')
    LOGGER.info('appFilePrefix = %s' % config['appFilePrefix'])
    retCode = RET_OK

    # print current environment
    retCode, output = execSystemCommandRunAs('env', runas)
    LOGGER.debug('current environment: %s' % (output))
    Logger().log('current environment: %s' % output, True)


    # download file
    retCode = downloadFile(pkgUrl, config['destFile'])
    recordStageLog(config['taskId'], 'downloadFile', retCode)
    if retCode != RET_OK: return retCode

    # check file md5sum
    retCode = checkFileMd5sum(config['destFile'], md5sum)
    recordStageLog(config['taskId'], 'checkMd5sum', retCode)
    if retCode != RET_OK:
        uploadLog(config['taskId'], 'checkMd5sum...failed')
        return retCode
    else:
        uploadLog(config['taskId'], 'checkMd5sum...success')

    if serviceType == 'html':
        config['publishPath'] = '/home/admin/website/'
        retCode = publishHtmlService(config, runas)
    elif serviceType == 'tomcat':
        config['stopServiceCommand'] = '/usr/local/tomcat/bin/shutdown.sh'
        config['startServiceCommand'] = '/usr/local/tomcat/bin/startup.sh'
        config['stopTengineCommand'] = 'sudo /etc/init.d/tengine stop'
        config['startTengineCommand'] = 'sudo /etc/init.d/tengine start'
        config['publishPath'] = '/usr/local/tomcat/webapps/'
        Logger().log(config, True)
        retCode = publishTomcatService(config, runas)
    elif serviceType == 'apijar':
        config['stopServiceCommand'] = '/usr/local/tomcat/bin/shutdown.sh'
        config['startServiceCommand'] = '/usr/local/tomcat/bin/startup.sh'
        config['stopTengineCommand'] = 'sudo /etc/init.d/tengine stop'
        config['startTengineCommand'] = 'sudo /etc/init.d/tengine start'
        config['publishPath'] = '/home/admin/api/'
        retCode = publishApijarService(config, runas)
    else:
        config['stopServiceCommand'] = '/home/admin/%s/service.sh' % (config['appFilePrefix'])
        config['startServiceCommand'] = '/home/admin/%s/service.sh' % (config['appFilePrefix'])
        config['publishPath'] = '/home/admin/'
        retCode = publishCommonService(config, runas)
 
    if retCode != RET_OK: return retCode

    # complete
    msg = '发布完成;'
    LOGGER.info('publishing finished, all is well, thank goodness!')
    commitTaskStatus(taskId, msg, RET_FINISHED)
    clean(config['tempDir'])

    return RET_OK

def run(pkgUrl, md5sum, taskId, serviceType, runas='admin'):
    Logger()
    if not os.path.exists(run_log_file):
        os.mknod(run_log_file)
    if not os.path.exists(error_log_file):
        os.mknod(error_log_file)

    retCode = RET_OK
    try:
        os.chdir(HOME_DIR)
        os.environ['JAVA_HOME']='/usr/local/jdk'
        os.environ['HOME']=HOME_DIR
        os.environ['PATH']='/usr/local/jdk/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/zabbix/bin:/usr/local/zabbix/sbin'
        #setRunningUser(RUNNING_USER)
        global LOGGER
        LOGGER = initLogger(LOGGER_FILE)
        LOGGER.info('uid: %s %s' % (os.getuid(),os.geteuid()))
        LOGGER.info('chdir: %s' % (os.getcwd()))
        LOGGER.info(str(os.environ))
        Logger().log(str(os.environ), True)
        retCode = runTask(pkgUrl, md5sum, taskId, serviceType, runas=RUNNING_USER)
    except Exception, e:
        retCode = RET_ERROR_RUN_EXCEPTION
        tb = traceback.format_exc()
        LOGGER.info('%s %s' %(str(tb), str(e)))
        msg = '发布异常'
        commitTaskStatus(taskId, msg, retCode)

    return retCode

def uploadMd5(pkgUrl, taskId):
    retCode = RET_OK
    auth_key = 'vLCzbZjGVNKWPxqd'

    try:
        with open(pkgUrl) as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()

        msg = {'id': taskId, 'md5': md5}
        msg = json.dumps(msg)
        response = requests.post(
            url=API_URL,
            headers={'key': AUTH_KEY},
            json=msg,
        )
        Logger().log('%s--%s' % (pkgUrl, md5) , True)
    except Exception, e:
        return e
    return retCode

def uploadLog(taskId, msg):
    """
    上传日志到Cmdb API ReleaseLog
    :param taskId:
    :param msg:
    :return:
    """
    retCode = RET_OK

    try:
        msg = {'id': taskId, 'msg': msg}
        msg = json.dumps(msg)
        response = requests.post(
            url=API_URL,
            headers={'key': AUTH_KEY},
            json=msg,
        )
        Logger().log('[%s]-[%s]日志上传成功...' % (taskId, msg), True)

    except Exception, e:
        Logger().log('[%s]-[%s]日志上传失败...' % (taskId, msg), True)
        Logger().log('[%s]-[%s]日志上传失败...' % (taskId, msg), False)
        recordStageLog(taskId, 'uploadLog', 'failed', e)

    return retCode

def ExecCmd(cmd):
    """
    执行本地shell命令
    :param cmd:
    :return:
    """
    ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    out, err = ret.communicate()
    if err:
        err = str(err)
        print('ERROR-->', err)
        return 1, err
    else:
        out = str(out)
        return 0, out


def JenkinsModify(pkg_name, task_id, release_git_url, release_branch, name, env, pack_cmd):
    """
    模拟Jenkins功能 拉代码 + 打包
    :return:
    """
    Logger()
    retCode = 0
    uploadLog(task_id, '连接成功......开始拉取代码')
    # 拉去代码
    # ('/data/packages/infra/cmdb/107/infra_cmdb_107.war', '107', 'http://gitlab.xxd.com/service/v6_batch.git', 'master', 'cmdb', 'infra')
    # print(pkg_name, task_id, release_git_url, release_branch, name, env)
    workspace_path = '%s%s' % (CMDB_WORKSPACE, name)
    pkg_path = os.path.dirname(pkg_name)
    if not os.path.exists(pkg_path):
        os.makedirs(pkg_path)
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    os.chdir(workspace_path)
    cmd = 'git init'
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = 'git config remote.origin.url %s' % release_git_url
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = 'git fetch --tags --progress %s +refs/heads/*:refs/remotes/origin/* > /dev/null 2>&1' % release_git_url
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = 'git rev-parse origin/%s' % release_branch
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = 'git checkout -f %s > /dev/null 2>&1' % out
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)

    cmd = "find ./ -name 'pom.xml' | xargs -I {} sh -c 'pom_dir=`dirname {}` && cd $pom_dir && %s>> %s'" % (env, pack_cmd,run_log_file)
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    os.chdir(workspace_path)

    cmd = "find ./ -name '*.war' -exec cp {} %s \;" % pkg_path
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    ret = uploadMd5(pkg_name, task_id)
    if ret:
        Logger().log('create md5 failed...', True)
        return ret

    return retCode

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # Jenkins端打包完毕后上传MD5值
        retCode = uploadMd5(sys.argv[1], sys.argv[2])
        sys.exit(retCode)
    # 集成Jenkins功能
    if len(sys.argv) == 8:
        retCode = JenkinsModify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
        sys.exit(retCode)
    if len(sys.argv) != 5:
        print "Miss arguments."
        sys.exit(1)
    # build.xxd.com/infra/cmdb/97/infra_cmdb_97.war 6d200fd40a846900c72574e0521b7e26 97 tomcat
    # print sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    retCode = run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    exit(retCode)
    # exit(0)


