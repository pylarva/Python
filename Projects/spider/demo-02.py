# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import pandas as pd


headers = {
    'authorization': "Bearer 2|1:0|10:1521100313|4:z_c0|92:Mi4xaGNVbEFnQUFBQUFBd0N4NTF6eEtEU1lBQUFCZ0FsVk5HWFNYV3dBYlNDU1pqOFNMSWdMcWhOUm1NVUxsRThMdUJ3|75b11eabdfb336b50b2d6b813d317c4994adae70da13f8e9b177931bdae701e4",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}

url = "https://www.zhihu.com/api/v4/members/crossin/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20"

response = requests.get(url, headers=headers).json()['data']
df = pd.DataFrame.from_dict(response)
df.to_excel('user.xlsx')

