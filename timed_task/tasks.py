#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from timed_task.celery import app
from bs4 import BeautifulSoup
import requests
from hello import db,News,Attachments
import re

@app.task

def add(x, y):

    return x + y

@app.task
def store_sse_news():
    soup=BeautifulSoup(requests.get('http://sse.tongji.edu.cn/InfoCenter/Lastest_Notice.aspx').text, "lxml")
    news=soup.find_all('div', attrs={"class": "news"})

    for new in news:

        if (News.query.filter_by(url=new.div.a['href'].replace('..','http://sse.tongji.edu.cn/')).first()):
            pass
        else:


            new=News(website='sse',title=new.div.a.string,url=new.div.a['href'].replace('..','http://sse.tongji.edu.cn/'),date=new.span.string)
            detail_new=store_detail_news(new)
            db.session.add(detail_new)
            db.session.commit()




def store_detail_news(new):
    response = requests.get(new.url)
    soup = BeautifulSoup(response.text, "lxml")
    detail_new=soup.find(id='content')
    if (detail_new):
        tables=detail_new.find_all('table')
        if(tables):
            text=''
            for child in detail_new.contents:
                if (child.name == 'table'):
                    for tr in child.find_all('tr'):
                        text = text + re.sub('(\n){1,}', '&nbsp;', tr.get_text().strip()) + '<br>'
                else:
                    if (child.name != None):              #有一些是注释，需要排除注释
                        str = child.get_text().replace(u'\xa0', '&nbsp;').replace('\n', '<br>')
                        if (str[-4:] != '<br>'):          #有一些行末没有换行符
                            text = text + str + '<br>'
                        else:
                            text = text + str
            new.text = text

        else:
            new.text= (detail_new.get_text().replace(u'\xa0', '&nbsp;').replace('\n','<br>'))


    attaches_new=soup.find(id='attachment').find_all('li')
    if (attaches_new):
        for attach in attaches_new:
            attachment=Attachments(name=attach.a.string,url=attach.a['href'].replace('..','http://sse.tongji.edu.cn'),news=new)
            db.session.add(attachment)
            db.session.commit()
            # print(attach.a.string)
            # print(attach.a['href'].replace('..','http://sse.tongji.edu.cn'))
    return new
