
import json
import hashlib
import requests

API_URL = 'http://0.0.0.0:8005/api/install'
ASSET_AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'


def auth_key():
    """
    接口认证
    :return:
    """
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s" % ASSET_AUTH_KEY, encoding='utf-8'))
    encryption = ha.hexdigest()
    result = "%s" % encryption
    return {"AUTH": result}


def upload_log(install_id, msg):
    """
    装机过程中上传日志
    :param install_id:
    :param msg:
    :return:
    """
    headers = {}
    headers.update(auth_key())

    msg = {'id': install_id, 'msg': msg}
    msg = json.dumps(msg)
    response = requests.post(
        url=API_URL,
        headers=headers,
        json=msg,
    )
    print(json.loads(response.text))

if __name__ == '__main__':
    upload_log('15', 'This is a test msg...')


