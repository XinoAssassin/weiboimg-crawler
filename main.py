'''微博配图爬虫'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
from imgdownloader import writedata

API = 'http://m.weibo.cn/container/getIndex?'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

def cardinfo(nick, card):
    '''写数据库并下载配图'''
    if card['card_type'] == 11:
        return 302
    if card['mblog'].get('retweeted_status'):
        # 跳过转发内容
        pass
    elif card['mblog'].get('pics'):
        weibolink = card['scheme']
        # 过滤微博内容中的超链接
        weibotext = re.sub('<.+?>', '', card['mblog']['text'])
        weibopics = card['mblog'].get('pics')
        # weibogifs = card['mblog']['gif_ids'].replace(',', '|')
        # weibogifs = [x for x in weibogifs.split('|')]
        weibopics = [x.get('large')['url'] for x in weibopics]
        writedata(nick, weibolink, weibotext, weibopics)
    else:
        pass


def getcontent(nick):
    '''API接口获取微博内容'''
    indexurl = 'http://m.weibo.cn/n/{nick}'.format(nick=nick)
    weibocokie = requests.get(url=indexurl).headers.get('Set-Cookie')
    weibofid = re.findall(r'\d{16}', weibocokie)[0]
    usercont = requests.get(url=API + 'containerid={0}'.format(weibofid)).json()
    usertabs = usercont['tabsInfo']['tabs']
    for tab in usertabs:
        if tab.get('title') == "微博":
            containerid = tab.get('containerid')
    page = 1
    params = {'containerid': containerid}
    weibocont = requests.get(url=API, headers=HEADERS, params=params).json()
    print(containerid)
    while weibocont.get('ok') == 1:
        if weibocont.get('cards'):
            contentcards = weibocont.get('cards')
            for card in contentcards:
                cardinfo(nick, card)
        else:
            break
        page += 1
        params = {'containerid': containerid, 'page': page}
        weibocont = requests.get(url=API, headers=HEADERS, params=params).json()


if __name__ == '__main__':
    for name in open('nickname.txt'):
        name = name.strip('\n').strip('\r')
        getcontent(name)
