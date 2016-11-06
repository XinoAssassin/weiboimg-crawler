#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sqlite3
import multiprocessing
import os

def Downloader(pic_id=None,gif=None):
    if gif == 1:
        url = "http://ww4.sinaimg.cn/large/{pic_id}.gif".format(pic_id=pic_id)
        filename = pic_id + '.gif'
    else:
        url = "http://ww4.sinaimg.cn/large/{pic_id}.jpg".format(pic_id=pic_id)
        filename = pic_id + '.jpg'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
    file = requests.get(url=url, headers=headers)
    print(u'正在下载 {filename}'.format(filename=filename))
    if os.path.exists(filename):
        print(u'{filename} 已存在，跳过下载过程'.format(filename=filename))
    else:
        with open(filename, 'wb') as f:
            f.write(file.content)
        f.close()


def WriteData(nickname=None, created_at=None, text=None, pic_ids=None, gif_ids=None):
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
        if not gif_ids:
            t = multiprocessing.Process(target=Downloader, args=(pic_id, 0))
        elif pic_id in gif_ids:
            t = multiprocessing.Process(target=Downloader, args=(pic_id, 1))
        else:
            t = multiprocessing.Process(target=Downloader, args=(pic_id, 0))
        t.start()