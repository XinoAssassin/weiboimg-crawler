#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import json
import os
from bs4 import BeautifulSoup
from imgdownloader import WriteData


def GetID(nickname=None):
    if nickname:
        url = 'http://m.weibo.cn/n/{nickname}'.format(nickname=nickname)
    else:
        return 404
    try:
        tmp = requests.get(url=url)
        m_page = BeautifulSoup(tmp.text, "lxml")
        fid = re.findall(fid_re, m_page.body.script.text)[0]
        return int(fid)
    except ValueError:
        return 404


def PageCount(url=None):
    # Return Page Number
    tmp = requests.get(url=url)
    try:
        content = json.loads(tmp.text)
        if content['ok'] == 1:
            total_w = content['count']
            page = total_w // 10 if total_w % 10 == 0 else total_w // 10 + 1
            return page
        else:
            # Unknow Error?
            pass
    except ValueError:
        return None


def CardInfo(nickname=None, card=None):
    # Original Weibo Only
    if card['mblog'].get('retweeted_status'):
        pass
    elif card['mblog']['pic_ids']:
        created_at = card['mblog']['created_at']
        # Need Text Only
        text = re.sub('<.+?>', '', card['mblog']['text'])
        pic_ids = card['mblog']['pic_ids']
        gifs = card['mblog']['gif_ids'].replace(',', '|')
        gif_ids = [x for x in gifs.split('|')]
        WriteData(nickname, created_at, text, pic_ids, gif_ids)
    else:
        pass


def GetJson(nickname=None, fid=None, page=None):
    if fid:
        url = 'http://m.weibo.cn/page/json?containerid={fid}_-_WEIBO_SECOND_PROFILE_WEIBO'.format(fid=fid)
    else:
        return 404
    if page:
        url += '&page={page}'.format(page=page)
    else:
        # If page, Get data, If not, Get page
        return PageCount(url=url)
    tmp = requests.get(url=url)
    try:
        content = json.loads(tmp.text)
        if content['ok'] == 1:
            if content['cards'][0]['mod_type'] == "mod/empty":
                return 200
            else:
                card_group = content['cards'][0]['card_group']
                for card in card_group:
                    CardInfo(nickname, card)
        else:
            # Unknow Error
            pass
    except ValueError:
        return None


if __name__ == '__main__':
    fid_re = re.compile(r"stageId\':\'(\d+)")
    for nickname in open('nickname.txt'):
        nickname = nickname.strip('\n').strip('\r')
        if os.path.exists(nickname):
            os.chdir(nickname)
        else:
            os.mkdir(nickname)
            os.chdir(nickname)
        page = GetJson(GetID(nickname))
        fid = GetID(nickname)
        if page:
            for x in range(1, page + 1):
                GetJson(nickname, fid, x)
            os.chdir('..')
        else:
            pass