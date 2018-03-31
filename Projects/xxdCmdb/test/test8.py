
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
    # 返回字典key好像只能是AUTH 否则request.environ里面添加失败
    return {"AUTH": result}


install_id = '1'
msg = 'test001.....'
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


