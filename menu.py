#!/usr/bin/python
# -*- coding: utf-8 -*-
import  urllib2
import json
AppID='wxa0010552b715c567'
AppSecret='3b29db69b0b6bcd450c3c61b9e1c4ee4'

def token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        AppID, AppSecret)
    result = urllib2.urlopen(url).read()
    access_token = json.loads(result).get('access_token')
    return   access_token


def createMenu():
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % token()
    data = {
        "button": [


            {
                "type": "view",
                "name": "软院信息",
                "url": "http://118.190.72.14/index"

            }

        ]
    }

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data))
