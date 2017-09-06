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
# API_URL = 'http://192.168.33.110:8005/api/release'
API_URL = 'http://172.16.19.12:8005/api/release'
# API_URL = 'http://cmdb.xinxindai.com/api/release'
TMP_DIR = '/tmp'
LOGGER_FILE = '/home/admin/logs/autopublishing.log'
RUNNING_USER = 'admin'
HOME_DIR = '/home/admin'
LOGGER = None
AUTH_KEY = 'vLCzbZjGVNKWPxqd'
CMDB_WORKSPACE = '/root/.cmdb/workspace/'
run_log_file = '/home/admin/logs/run.log'
error_log_file = '/home/admin/logs/err.log'
CHECK_SERVICE_TIMEOUT = 30

# 配置文件源目录路径
config_scource_path = '/opt/config/prod/'
# 配置文件目标目录路径
config_target_path = '/usr/local/tomcat/webapps/AAA/WEB-INF/classes/'

# 需要向nginx上发布静态资源的项目列表和默认发布目录
static_nginx_dict = ['front', 'webapp']

# 需要ROOT目录的项目列表
ROOT_obj = ['front', 'seo', 'webapi', 'sso', 'shorturl', 'fk']

# 项目名与路径不一致项目列表
Diff_obj = {'front': 'ROOT', 'seo': 'ROOT', 'webapi': 'ROOT', 'sso': 'ROOT', 'shorturl': 'ROOT', 'webapp': 'm', 'fk': 'ROOT'}

# 新建软链项目列表
soft_link_list = {'front':'ROOT', 'xxdai_sys_admin': 'xxdai_sys_admin', 'seo': 'ROOT', 'webapp': 'm', 'v5_mobile': 'v5_mobile'}

# 打包不需要 -P 参数的项目列表
pkg_cmd_no_p_list = ['webapp', 'xxdai_sys_admin', 'xxdai_batch', 'credit_app', 'finance', 'v5_mobile', 'seo', 'xxdai_tradews', 'yx_service', 'front']

# Java环境变量
java_version_path = {'1': '/usr/local/jdk8', '2': '/usr/local/jdk7', '3': '/usr/java/jdk1.6.0_32'}

# 发布静态资源项目打包命令列表
static_pkg_cmd_list = {'mui': 'cnpm install && gulp && cd pages/ && /usr/bin/zip -r build.zip build && /bin/cp build.zip ',
                       'mobile': 'cnpm install && gulp && /usr/bin/zip -r html.zip html && /bin/cp html.zip ',
                       'html': 'cnpm install && gulp && /usr/bin/zip -r html.zip html && /bin/cp html.zip ',
                       'pc': 'cnpm install && gulp && cd pages/ && /usr/bin/zip -r build.zip build && /bin/cp build.zip ',
                       'heidai': 'cnpm install && gulp && /usr/bin/zip -r html.zip html && /bin/cp build.zip ',
                       'digital': 'mv pages digital && /usr/bin/zip -r digital.zip digital && /bin/cp digital.zip ',
                       'm': 'cnpm install && npm run build && /usr/bin/zip -r dist.zip dist && /bin/cp dist.zip '}

# 'static_m': 'cnpm install && npm run build && /usr/bin/zip -r dist.zip dist && /bin/cp dist.zip

static_pkg_name = {'mui': 'build', 'mobile': 'html', 'html': 'html', 'pc': 'build', 'apk': 'apk', 'm': 'dist'}

# apk 放置目录
apk_path = '/opt/static/download/'

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
        regex = '^%s' % filename
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

def downloadFile(path, dest, task_id):
    # dir = os.path.dirname(dest)
    # try:
    #     cmd = 'wget %s -P %s' % (path, dir)
    #     ret, out = ExecCmd(cmd)
    #     Logger().log(cmd, True)
    #     Logger().log(out, True)
    #     if ret:
    #         Logger().log(out, False)
    #         return out
    # except Exception, e:
    #     Logger().log(e, True)
    try:
        ul = urllib.URLopener()
        ul.retrieve(path, dest)
        Logger().log('%s->%s' % (path, dest), True)
        uploadLog(task_id, 'Download success..%s->%s' % (path, dest))
    except Exception, e:
        LOGGER.info('Download file failed: %s, exception: %s' % (path, e))
        Logger().log('Dowanload %s -> %s err --> %s' % (path, dest, e), True)
        Logger().log('Dowanload %s -> %s err --> %s' % (path, dest, e), False)
        uploadLog(task_id, 'Dowanload %s -> %s err --> %s' % (path, dest, e))
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


def checkApiService(ip, taskId):
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
            cmd = "curl -I -m 5 %s:8080" % ip
            ret = os.system(cmd)
            if ret == 0:
                Logger().log('check services --> Java start success....', True)
                return 0
            else:
                Logger().log('check services --> try to start....%s' % total_time, True)
                continue
        Logger().log('check services --> Java start timeout....', True)
        Logger().log('check services --> Java start timeout....', False)
        uploadLog('chechk service --> Java start timeout...', taskId)
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

def createSoftLink(name):
    if name in soft_link_list:
        Logger().log('%s need create soft link...' % name, True)
        try:
            if name in ROOT_obj:

                cmd = 'mkdir -p /usr/local/tomcat/webapps/ROOT/static/admin/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/ROOT/static/image'
                ret, out = ExecCmd(cmd)
                # os.system(cmd)
                # Logger().log(cmd, True)
                Logger().log('%s --> %s' % (cmd, out), True)

                cmd = 'ln -s /opt/webapps/front/image /usr/local/tomcat/webapps/ROOT/static/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/ROOT/static/admin/image'
                ret, out = ExecCmd(cmd)

                cmd = 'mkdir -p /usr/local/tomcat/webapps/ROOT/static/admin/'
                ret, out = ExecCmd(cmd)

                cmd = 'ln -s /opt/webapps/admin/image /usr/local/tomcat/webapps/ROOT/static/admin/'
                ret, out = ExecCmd(cmd)

            elif name == 'xxdai_sys_admin':

                cmd = 'rm -fr /usr/local/tomcat/webapps/xxdai_sys_admin/image'
                ret, out = ExecCmd(cmd)
                cmd = 'ln -s /opt/webapps/admin/image/ /usr/local/tomcat/webapps/xxdai_sys_admin/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/xxdai_sys_admin/images'
                ret, out = ExecCmd(cmd)
                cmd = 'ln -s /opt/webapps/admin/images /usr/local/tomcat/webapps/xxdai_sys_admin/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/xxdai_sys_admin/frontimg/'
                ret, out = ExecCmd(cmd)
                cmd = 'ln -s /opt/webapps/front/frontimg /usr/local/tomcat/webapps/xxdai_sys_admin/'
                ret, out = ExecCmd(cmd)



            elif name == 'webapp':

                cmd = 'rm -fr /usr/local/tomcat/webapps/m/static/image'
                ret, out = ExecCmd(cmd)
                Logger().log('%s --> %s' % (cmd, out), True)
                cmd = 'ln -s /opt/webapps/front/image /usr/local/tomcat/webapps/m/static/'
                ret, out = ExecCmd(cmd)
                Logger().log('%s --> %s' % (cmd, out), True)

            elif name == 'v5_mobile':
                cmd = 'mkdir -p /usr/local/tomcat/webapps/v5_mobile/static/admin/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/v5_mobile/static/image'
                ret, out = ExecCmd(cmd)
                cmd = 'ln -s /opt/webapps/front/image /usr/local/tomcat/webapps/v5_mobile/static/'
                ret, out = ExecCmd(cmd)

                cmd = 'rm -fr /usr/local/tomcat/webapps/v5_mobile/static/admin/image'
                ret, out = ExecCmd(cmd)

                cmd = 'ln -s /opt/webapps/admin/image/ /usr/local/tomcat/webapps/v5_mobile/static/admin/'
                ret, out = ExecCmd(cmd)

        except Exception, e:
            Logger().log('create soft link failed...%s' % e, True)
            Logger().log('create soft link failed...%s' % e, False)
            return 1
    return 0




def publishTomcatService(config, name, taskId, runas):
    retCode = RET_OK

    # if config['appFilePrefix'] == 'api':
    #     retCode, output = execSystemCommandRunAs(config['stopTengineCommand'], runas)
    #     recordStageLog(config['taskId'], 'stopTengineService', retCode, output)
    #     if retCode != RET_OK: return retCode

    # stop service
    if os.path.exists(config['stopServiceCommand']):
        cmd = 'ps -ef | grep java | wc -l'
        retCode, output = execSystemCommandRunAs(cmd, runas)
        out = output
        if out.split()[0] == '2':
            Logger().log('stop services --> Java process not start....', True)
        else:
            retCode, output = execSystemCommandRunAs(config['stopServiceCommand'], runas)
            Logger().log('stop service --> %s %s' % (retCode, output))
            recordStageLog(config['taskId'], 'stopService', retCode, output)
            time.sleep(3)

            # 如果java进程无法关闭 kill进程
            cmd = "ps -A"
            retCode, output = execSystemCommandRunAs(cmd, runas)
            s = 'java'
            for line in output.splitlines():
                if s in line:
                    pid = line.split()[0]
                    os.kill(int(pid), signal.SIGKILL)
                    Logger().log('kill pid --> %s' % pid)
        # if retCode != RET_OK: return retCode

    # clean old files
    # needCleanPath = os.path.join(config['publishPath'], config['appFilePrefix'])
    needCleanPath = config['destFile']
    Logger().log('destFile-->%s' % needCleanPath)
    if os.path.exists(needCleanPath):
        # retCode = moveFile(config['publishPath'], config['appFilePrefix'], config['tempDir'], matchPrefix=True)
        # recordStageLog(config['taskId'], 'cleanOldFiles', retCode)
        # if retCode != RET_OK: return retCode
        if os.path.exists('/opt/webapps_bak/'):
            cmd = '/bin/rm -fr /opt/webapps_bak/*'
            os.system(cmd)
        else:
            os.makedirs('/opt/webapps_bak/')
            cmd = 'chown admin.admin /opt/webapps_bak/'
            os.system(cmd)
        cmd = '/bin/mv %s* /opt/webapps_bak/' % (config['publishPath'])
        os.system(cmd)
        cmd = '/bin/rm -rf /usr/local/tomcat/webapps/*'
        os.system(cmd)
        cmd = '/bin/rm -rf /usr/local/tomcat/work/*'
        os.system(cmd)

    # publish files
    # 需要将代码放入ROOT文件夹的项目 ➡️ 新建ROOT目录
    if name in Diff_obj:
        publish_path = '/usr/local/tomcat/webapps/%s' % Diff_obj[name]
    else:
        publish_path = '/usr/local/tomcat/webapps/%s' % name

    if not os.path.exists(publish_path):
        os.makedirs(publish_path)
        os.system('chown -R admin.admin /usr/local/tomcat')
    else:
        cmd = 'rm -fr %s/*' % publish_path
        os.system(cmd)

    cmd = 'unzip -o %s -d %s > /dev/null 2>&1' % (config['destFile'], publish_path)
    os.system(cmd)
    Logger().log(cmd, True)

    # 启动服务之前 新建软链
    if name in soft_link_list:
        ret = createSoftLink(name)
        if ret != RET_OK: return ret

    # 拷贝配置文件
    config_path_name = '%s%s/' % (config_scource_path, name)
    try:
        if os.path.exists(config_path_name):
            if name in soft_link_list:
                config_target_path_new = config_target_path.replace('AAA', soft_link_list[name])
            else:
                config_target_path_new = config_target_path.replace('AAA', name)
            cmd = '/bin/cp -r %s* %s' % (config_path_name, config_target_path_new)
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log('The [ %s ] had copy config files to %s...' % (name, config_target_path_new), True)
        else:
            Logger().log('The [ %s ] does not need copy config files...' % name, True)
    except Exception, e:
        Logger().log('copy config failed...%s' % e, True)

    # 更改admin权限
    os.system('chown -R admin.admin /usr/local/tomcat')

    # start service
    uploadLog(taskId, '正在重启tomcat...')
    retCode, output = execSystemCommandRunAs(config['startServiceCommand'], runas, timeout=300)
    recordStageLog(config['taskId'], 'startService', retCode, output)
    if retCode != RET_OK:
        uploadLog(taskId, 'Tomcat start timeout...')
        return retCode

    if config['appFilePrefix'] == 'api':
        retCode, output = execSystemCommandRunAs(config['startTengineCommand'], runas)
        recordStageLog(config['taskId'], 'startTengineService', retCode, output)
        if retCode != RET_OK: return retCode

    # check service
    if config['appFilePrefix'] == 'api':
        retCode = checkApiService()
        recordStageLog(config['taskId'], 'checkService', retCode, '')

    retCode = checkApiService('0.0.0.0', taskId)
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

def runTask(pkgUrl, md5sum, taskId, serviceType, name, runas):
    # build.xxd.com/infra/cmdb/97/cmdb.war 6d200fd40a846900c72574e0521b7e26 97 tomcat
    config = {}
    url = urlparse.urlparse(pkgUrl)
    filename = os.path.basename(url.path)
    fileSuffix = filename.split('.')[-1]
    config['taskId'] = taskId
    config['appFilePrefix'] = filename.split('/')[-1]
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
    retCode = downloadFile(pkgUrl, config['destFile'], taskId)
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
        retCode = publishTomcatService(config, name, taskId,runas)
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

def run(pkgUrl, md5sum, taskId, serviceType, name, runas='admin'):
    # Logger()
    if not os.path.exists(run_log_file):
        os.mknod(run_log_file)
    if not os.path.exists(error_log_file):
        os.mknod(error_log_file)

    retCode = RET_OK
    try:
        os.chdir(HOME_DIR)
        # os.environ['JAVA_HOME']='/usr/local/jdk'
        # os.environ['HOME']=HOME_DIR
        # os.environ['PATH']='/usr/local/jdk/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/zabbix/bin:/usr/local/zabbix/sbin'
        # setRunningUser(RUNNING_USER)
        global LOGGER
        # LOGGER = initLogger(LOGGER_FILE)
        LOGGER.info('uid: %s %s' % (os.getuid(),os.geteuid()))
        LOGGER.info('chdir: %s' % (os.getcwd()))
        LOGGER.info(str(os.environ))
        Logger().log(str(os.environ), True)
        retCode = runTask(pkgUrl, md5sum, taskId, serviceType, name, runas=RUNNING_USER)
    except Exception, e:
        retCode = RET_ERROR_RUN_EXCEPTION
        tb = traceback.format_exc()
        LOGGER.info('%s %s' %(str(tb), str(e)))
        msg = '发布异常'
        commitTaskStatus(taskId, msg, retCode)

    return retCode

def uploadMd5(pkgUrl, taskId,):
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
        Logger().log('ERROR-->%s' % err, True)
        Logger().log('ERROR-->%s' % err, False)
        return 1, err
    else:
        out = str(out)
        return 0, out


def JenkinsModify(pkg_name, task_id, release_git_url, release_branch, name, env, pack_cmd, jdk_version, type, static_type):
    """
    模拟Jenkins功能 拉代码 + 打包
    :return:
    """
    retCode = 0
    uploadLog(task_id, '连接成功......开始拉取代码')
    Logger().log('[%s]连接成功......开始拉取代码'% task_id, True)

    # 设置环境变量
    os.chdir(HOME_DIR)

    os.environ['JAVA_HOME'] = java_version_path[jdk_version]
    os.environ['PATH']='%s/bin:/usr/local/maven/bin:/usr/local/node/bin:/usr/local/git/bin/:/usr/local/jdk7/bin:' \
                       '/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin' % java_version_path[jdk_version]

    cmd = 'export PATH=%s/bin/:$PATH' % java_version_path[jdk_version]

    os.environ['HOME'] = HOME_DIR
    os.system(cmd)

    if type == '2':
        cmd = 'export PATH=%s/bin/:$PATH' % '/usr/local/node'
        os.system(cmd)

    Logger().log(str(os.environ), True)

    # 拉取代码
    workspace_path = '%s%s' % (CMDB_WORKSPACE, name)
    pkg_path = os.path.dirname(pkg_name)
    if not os.path.exists(pkg_path):
        os.makedirs(pkg_path)
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)

    # Html项目不能在html文件路径下gulp
    if name == 'html':
        workspace_path = '%sxxd_html/' % CMDB_WORKSPACE
        if os.path.exists(workspace_path):
            cmd = 'rm -fr /root/.cmdb/workspace/xxd_html/*'
            os.system(cmd)
        else:
            cmd = 'mkdir -p %s' % workspace_path
            os.system(cmd)
        Logger().log(cmd, True)

    os.chdir(workspace_path)

    cmd = 'rm -fr /root/.cmdb/workspace/%s/*' % name
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    os.chdir(workspace_path)

    cmd = 'git init'
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = '/usr/local/git/bin/git rev-parse --is-inside-work-tree'
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    cmd = '/usr/local/git/bin/git config remote.origin.url %s' % release_git_url
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    if name == 'html':
        cmd = "ssh 127.0.0.1 'cd /root/.cmdb/workspace/xxd_html && /usr/local/git/bin/git fetch --tags --progress %s +refs/heads/*:refs/remotes/origin/* > /dev/null 2>&1'" % release_git_url
    else:
        cmd = "ssh 127.0.0.1 'cd /root/.cmdb/workspace/%s && /usr/local/git/bin/git fetch --tags --progress %s +refs/heads/*:refs/remotes/origin/* > /dev/null 2>&1'" % (name, release_git_url)
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    if 'tag' in release_branch:
        cmd = '/usr/local/git/bin/git rev-parse %s' % release_branch
    else:
        cmd = '/usr/local/git/bin/git rev-parse origin/%s' % release_branch

    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        uploadLog(task_id, '拉取代码失败...%s' % out)
        return out

    cmd = '/usr/local/git/bin/git checkout -f %s > /dev/null 2>&1' % out
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)

    # cmd = 'set -e'
    # os.system(cmd)
    # Logger().log('set -e', True)

    # 如果是发布静态资源 打包命令在配置文件里
    if type == '2':
        if name == 'apk':
            # 如果是apk项目 只需拉取文件 打包就行
            os.chdir(workspace_path)
            cmd = 'cd apk && zip apk.zip *'
            uploadLog(task_id, cmd)
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log(out, True)
            if ret:
                Logger().log(out, False)
                return out
            cmd = 'cd apk && /bin/cp -fr apk.zip %s' % pkg_path
            uploadLog(task_id, cmd)
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log(out, True)
            if ret:
                Logger().log(out, False)
                return out
            return 0
        os.chdir(workspace_path)
        cmd = '%s%s >> %s' % (static_pkg_cmd_list[name], pkg_path, run_log_file )
        uploadLog(task_id, cmd)
        uploadLog(task_id, '正在进行代码打包......')

        ret, out = ExecCmd(cmd)
        Logger().log(cmd, True)
        Logger().log(out, True)

        pkg_url = '%s/%s%s' % (pkg_path, static_pkg_name[name], '.zip')

        if os.path.exists(pkg_url):
            # 如果静态资源是迭代式发布 则需要更改发布的包名为版本好 如 1.1.8.zip
            # if static_type == '2':
            #     pkg_base = pkg_url.split('/')[-1]
            #     pkg_base_new = pkg_name.split('/')[-1]
            #     pkg_url_new = pkg_url.replace(pkg_base, pkg_base_new)

                # cmd = 'mv %s %s' % (pkg_url, pkg_url_new)
                # os.system(cmd)
                # Logger().log(cmd, True)

            ret = uploadMd5(pkg_url, task_id)
            if ret:
                Logger().log('create md5 failed...', True)
                return ret
            return 0
        else:
            uploadLog(task_id, '代码打包失败......')
            Logger().log('files not exist..%s' % pkg_url, True)
            return False
    # elif name == 'fk':
    #     pass
        # cmd = 'cd /root/.cmdb/Release && /bin/cp YX.war %sYX.war' % pkg_path
        # ret, out = ExecCmd(cmd)
        # Logger().log(cmd, True)
        # Logger().log(out, True)
        # if ret:
        #     Logger().log(out, False)
        #     return out
        # ret = uploadMd5(pkg_name, task_id)
        # if ret:
        #     Logger().log('create md5 failed...', True)
        #     return ret
        # return 0
    else:
        # 项目mvn打包如果不要 -P 参数则不加
        if name in pkg_cmd_no_p_list:
            cmd = "find ./ -name 'pom.xml' | xargs -I {} sh -c 'pom_dir=`dirname {}` && cd $pom_dir && %s >> %s'" % (pack_cmd,run_log_file)
        else:
            cmd = "find ./ -name 'pom.xml' | xargs -I {} sh -c 'pom_dir=`dirname {}` && cd $pom_dir && %s -P%s>> %s'" % (pack_cmd,env,run_log_file)
        uploadLog(task_id, cmd)
        uploadLog(task_id, '正在进行代码打包......')
        ret, out = ExecCmd(cmd)
        Logger().log(cmd, True)
        Logger().log(out, True)
        if ret:
            Logger().log(out, False)
            return out

    # 需要发布静态资源到nginx上的项目 v6_front写死了 后面改
    try:
        if name in static_nginx_dict:
            Logger().log('zip static --> %s/static.zip'% pkg_path, True)
            os.chdir(workspace_path)
            if name == 'front':
                # cmd = "find ./ -type d -name 'static' -exec jar -cf %s/static.zip {} \;" % pkg_path
                cmd = "cd /root/.cmdb/workspace/front/src/main/webapp/ && zip -r static.zip static && /bin/cp -r static.zip %s" % pkg_path
            if name == 'webapp':
                cmd = "cd /root/.cmdb/workspace/webapp/v6_webapp/trunk/target/v6_webapp/ && zip -r static.zip static && /bin/cp -r static.zip %s" % pkg_path
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log(out, True)
            if ret:
                Logger().log(out, False)
                return out
    except Exception,e:
        Logger().log(e, True)

    os.chdir(workspace_path)

    cmd = "find ./ -name '*.war' -exec cp {} %s \;" % pkg_name

    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    os.chdir(workspace_path)

    try:
        if name in static_nginx_dict:
            cmd = "find ./ -name 'static.zip' -exec cp {} %s \; " % pkg_path
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log(out, True)
            if ret:
                Logger().log(out, False)
                return out
    except Exception,e:
        Logger().log(e, True)

    ret = uploadMd5(pkg_name, task_id)
    if ret:
        Logger().log('create md5 failed...', True)
        return ret

    return retCode

def NginxStatic(name, pkgUrl, taskId, env, static_type, branch):

    dest_dir = '/static/%s/%s/' % (env, name)

    if os.path.exists(dest_dir):
        if static_type == '2':
            version_name = branch.split('/')[-1]
            dest_dir = '%s%s' % (dest_dir, version_name)
            cmd = 'mkdir -p %s' % dest_dir
            os.system(cmd)
            Logger().log(cmd, True)
            dest_file = '%s/%s' % (dest_dir, os.path.basename(pkgUrl))
            ret = downloadFile(pkgUrl, '%s', taskId) % dest_file
            if not ret:
                Logger().log('download files success...', True)
            else:
                Logger().log('download files failed...', True)

            cmd = 'unzip -o %s -d %s' % (dest_file, dest_dir)
            ret, out = ExecCmd(cmd)
            Logger().log(cmd, True)
            Logger().log(out, True)
            if ret:
                Logger().log(out, False)
                return out
            return 0
    else:
        os.makedirs(dest_dir)

    # 发布静态资源顺序 下载zip包 ➡️ 删除原有文件夹 ➡️ 解压 ➡️ 删除新zip包
    if name in static_nginx_dict:
        dest_file = '%s%s' % (dest_dir, 'static.zip')
    else:
        dest_file = '%s%s.zip' % (dest_dir, static_pkg_name[name])

    Logger().log('down to %s...' % dest_file, True)

    if os.path.isfile(dest_file):
        cmd = 'rm -fr %s' % dest_file
        ExecCmd(cmd)

    ret = downloadFile(pkgUrl, dest_file, taskId)
    if not ret:
        Logger().log('download files success...', True)
    else:
        Logger().log('download files failed...', True)

    cmd = "find %s. ! -name '*.zip' -exec rm -fr {} \;" % dest_dir
    Logger().log(cmd, True)
    os.system(cmd)
    time.sleep(1)

    if name == 'apk':
        if not os.path.exists(apk_path):
            os.system('mkdir -p %s' % apk_path)
        cmd = 'unzip -o %s -d %s' % (dest_file, apk_path)
        ret, out = ExecCmd(cmd)
        Logger().log(cmd, True)
        Logger().log(out, True)
        if ret:
            Logger().log(out, False)
            return out
        return 0

    cmd = 'unzip -o %s -d %s' % (dest_file, dest_dir)
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    if ret:
        Logger().log(out, False)
        return out

    if os.path.isfile(dest_file):
        cmd = 'rm -fr %s' % dest_file
        ExecCmd(cmd)

    return 0

if __name__ == '__main__':
    # global LOGGER
    LOGGER = initLogger(LOGGER_FILE)
    cmd  = 'cd /home/admin/logs/ && touch %s %s %s' % (run_log_file, error_log_file, 'autopublishing.log')
    Logger()
    ret, out = ExecCmd(cmd)
    Logger().log(cmd, True)
    Logger().log(out, True)
    Logger().log('%s' % sys.argv, True)
    Logger().log('%s' % len(sys.argv), True)

    # 向Nginx发布静态资源
    if len(sys.argv) == 7:
        retCode = NginxStatic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        Logger().log('exit --> %s' % retCode)
        sys.exit(retCode)
    # 集成Jenkins功能
    if len(sys.argv) == 11:
        retCode = JenkinsModify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])
        sys.exit(retCode)
    # Tomcat项目发布
    if len(sys.argv) != 6:
        print "Miss arguments."
        sys.exit(1)
    retCode = run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    exit(retCode)
    # exit(0)


