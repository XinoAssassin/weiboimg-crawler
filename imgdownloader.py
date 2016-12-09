'''微博配图爬虫'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing
import os
import sqlite3
import requests

multiprocessing.freeze_support()


def downloader(picid, belong):
    '''专心下载'''
    workpath = os.path.abspath('.')
    if not picid:
        return 404
    else:
        filename = picid.split('/')[-1]
    if os.path.exists(belong):
        pass
    else:
        os.mkdir(belong)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
    file = requests.get(url=picid, headers=headers)
    filesize = file.headers.get('Content-Length')
    os.chdir(belong)
    if os.path.exists(filename) and (os.path.getsize(filename) == int(filesize)):
        print(u'{0} 已存在，跳过下载过程'.format(filename))
    else:
        filepath = workpath + '\\' + belong + '\\' + filename
        with open(filepath, 'wb') as imgfile:
            print(u'正在下载 {0}'.format(filename))
            imgfile.write(file.content)
        imgfile.close()
    os.chdir(workpath)


def writedata(nick, link, text, pics):
    '''写数据库'''
    weibodata = sqlite3.connect('weibo.db')
    localdb = weibodata.cursor()
    localdb.execute('CREATE TABLE IF NOT EXISTS weibolist \
    (Nick CHAR(40), WeiboLink CHAR(40), WeiboText CHAR(1000), ImageLink CHAR(80) PRIMARY KEY)')
    ins = 'INSERT OR REPLACE INTO weibolist VALUES(?, ?, ?, ?)'
    for pic in pics:
        worker = multiprocessing.Process(target=downloader, args=(pic, nick))
        localdb.execute(ins, (nick, link, text, pic))
        weibodata.commit()
        worker.start()
