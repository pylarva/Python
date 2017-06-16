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
from threading import Timer

API_HOST = 'cmdb.xxd.com'
API_URL = 'http://172.16.18.30:8005/api/release'
TMP_DIR = '/tmp'
LOGGER_FILE = '/home/admin/logs/autopublishing.log'
RUNNING_USER = 'admin'
HOME_DIR = '/home/admin'
LOGGER = None


# define return code
RET_OK = 0
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

# stage info
STAGE_MESSAGE_INFO = {
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

    if currentMd5sum != md5sum:
        return RET_ERROR_CHECK_FILE_MD5SUM_FAILED

    return RET_OK

def downloadFile(path, dest):
    ul =urllib.URLopener()
    try:
        ul.retrieve(path, dest)
    except IOError, e:
        LOGGER.info('Download file failed: %s, exception: %s' %(path, str(e)))
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


def checkApiService():
    retCode = RET_ERROR_CHECK_SERVICE_FAILED
    return retCode


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

    if config['appFilePrefix'] == 'api':
        retCode, output = execSystemCommandRunAs(config['stopTengineCommand'], runas)
        recordStageLog(config['taskId'], 'stopTengineService', retCode, output)
        if retCode != RET_OK: return retCode

    # stop service
    if os.path.exists(config['stopServiceCommand']):
        retCode, output = execSystemCommandRunAs(config['stopServiceCommand'], runas)
        recordStageLog(config['taskId'], 'stopService', retCode, output)
        if retCode != RET_OK: return retCode

    # clean old files
    needCleanPath = os.path.join(config['publishPath'], config['appFilePrefix'])
    if os.path.exists(needCleanPath):
        retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=True)
        recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
        if retCode != RET_OK: return retCode
        cmd = '/bin/rm -rf %s/ROOT' %(config['publishPath'])
        retCode, output = execSystemCommandRunAs(cmd, runas)

    # publish files
    cmd = '/bin/cp %s %s/%s.war' %(config['destFile'], config['publishPath'], config['appFilePrefix'])
    retCode, output = execSystemCommandRunAs(cmd, runas)
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
    if retCode != RET_OK: return retCode

    #start tengine
    if os.path.exists(config['startTengineCommand']):
        retCode, output = execSystemCommandRunAs(config['startTengineCommand'], runas)
        recordStageLog(config['taskId'], 'startTengineService', retCode, output)
        if retCode != RET_OK: return retCode

    # check service
    retCode = checkApiService()
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
    config = {}
    url = urlparse.urlparse(pkgUrl)
    filename = os.path.basename(url.path)
    fileSuffix = filename.split('.')[-1]
    config['taskId'] = taskId
    config['appFilePrefix'] = filename.split('_')[0]
    config['tempDir'] = tempfile.mkdtemp(prefix='%s-' %config['appFilePrefix'], dir='/tmp/')
    config['destFile'] = os.path.join(config['tempDir'], filename)
    os.chmod(config['tempDir'], stat.S_IRWXG+stat.S_IRWXO+stat.S_IRWXU)

    LOGGER.info('=== start publishing ===')
    LOGGER.info('appFilePrefix = %s' %config['appFilePrefix'])
    retCode = RET_OK

    # print current environment
    retCode, output = execSystemCommandRunAs('env', runas)
    LOGGER.debug('current environment: %s' %(output))

    # download file
    retCode = downloadFile(pkgUrl, config['destFile'])
    recordStageLog(config['taskId'], 'downloadFile', retCode)
    if retCode != RET_OK: return retCode

    # check file md5sum
    retCode = checkFileMd5sum(config['destFile'], md5sum)
    recordStageLog(config['taskId'], 'checkMd5sum', retCode)
    if retCode != RET_OK: return retCode

    if serviceType == 'html':
        config['publishPath'] = '/home/admin/website/'
        retCode = publishHtmlService(config, runas)
    elif serviceType == 'tomcat':
        config['stopServiceCommand'] = '/usr/local/tomcat/bin/shutdown.sh'
        config['startServiceCommand'] = '/usr/local/tomcat/bin/startup.sh'
        config['stopTengineCommand'] = 'sudo /etc/init.d/tengine stop'
        config['startTengineCommand'] = 'sudo /etc/init.d/tengine start'
        config['publishPath'] = '/usr/local/tomcat/webapps/'
        retCode = publishTomcatService(config, runas)
    elif serviceType == 'apijar':
        config['stopServiceCommand'] = '/usr/local/tomcat/bin/shutdown.sh'
        config['startServiceCommand'] = '/usr/local/tomcat/bin/startup.sh'
        config['stopTengineCommand'] = 'sudo /etc/init.d/tengine stop'
        config['startTengineCommand'] = 'sudo /etc/init.d/tengine start'
        config['publishPath'] = '/home/admin/api/'
        retCode = publishApijarService(config, runas)
    else:
        config['stopServiceCommand'] = '/home/admin/%s/service.sh' %(config['appFilePrefix'])
        config['startServiceCommand'] = '/home/admin/%s/service.sh' %(config['appFilePrefix'])
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
    retCode = RET_OK
    try:
        os.chdir(HOME_DIR)
        os.environ['JAVA_HOME']='/usr/local/jdk'
        os.environ['HOME']=HOME_DIR
        os.environ['PATH']='/usr/local/jdk/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/zabbix/bin:/usr/local/zabbix/sbin'
        #setRunningUser(RUNNING_USER)
        global LOGGER
        LOGGER = initLogger(LOGGER_FILE)
        LOGGER.info('uid: %s %s' %(os.getuid(),os.geteuid()))
        LOGGER.info('chdir: %s' %(os.getcwd()))
        LOGGER.info(str(os.environ))
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

    with open(pkgUrl) as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()

    msg = {'id': taskId, 'md5': md5}
    msg = json.dumps(msg)
    response = requests.post(
        url=API_URL,
        headers={'key': auth_key},
        json=msg,
    )
    print md5
    return retCode

if __name__ == '__main__':
    if len(sys.argv) == 3:
        retCode = uploadMd5(sys.argv[1], sys.argv[2])
        sys.exit(retCode)
    if len(sys.argv) != 5:
        print "Miss arguments."
        sys.exit(1)
    retCode = run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    exit(retCode)
