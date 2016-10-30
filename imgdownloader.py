#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sqlite3
import multiprocessing
import os

def Downloader(pic_id=None):
    url = "http://ww4.sinaimg.cn/large/{pic_id}.jpg".format(pic_id=pic_id)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
    file = requests.get(url=url, headers=headers)
    print(u'正在下载 {pic_id}.jpg'.format(pic_id=pic_id))
    filename = pic_id + '.jpg'
    if os.path.exists(filename):
        return 200
    with open(filename, 'wb') as f:
        f.write(file.content)
    f.close()


def WriteData(nickname=None, created_at=None, text=None, pic_ids=None):
    pic_db = sqlite3.connect('{nickname}.db'.format(nickname=nickname))
    curs = pic_db.cursor()
    curs.execute('CREATE TABLE IF NOT EXISTS weibolist (Id CHAR(40) PRIMARY KEY, WeiboText CHAR(200), Created_at CHAR(20))')
    ins = 'INSERT OR REPLACE INTO weibolist VALUES(?, ?, ?)'
    for pic_id in pic_ids:
        curs.execute(ins, (pic_id, text, created_at))
    pic_db.commit()
    curs.close()
    pic_db.close()
    for pic_id in pic_ids:
        t = multiprocessing.Process(target=Downloader, args=(pic_id,))
        t.start()