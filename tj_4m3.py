#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from hello import db,News,Attachments

def store_4m3_news():
    soup = BeautifulSoup(open('4m3.html', encoding='utf-8'), "lxml")
    news_table = soup.select('#module760241187 > div > table > tbody > tr')
    for tr in news_table[1:]:
        tds = tr.find_all('td')
        print(tds[0].string)
        pattern = re.compile('\d+')
        match = pattern.search(tds[0].a['onclick'])
        print(match.group())
        news_title = tds[0].string
        news_url = 'http://4m3.tongji.edu.cn/eams/noticeDocument!info.action?ifMain=1&notice.id=' + match.group()
        news_date = tds[2].string
        print(tds[2].string)

        new = News(website='4m3', title=news_title, url=news_url, date=news_date)
        detail_new = store_detail_news(new)
        db.session.add(detail_new)
        db.session.commit()

def store_detail_news(new):
    response = requests.get(new.url)
    soup = BeautifulSoup(response.text, "lxml")
    detail_new = soup.select('#studentInfoTable > tbody > tr:nth-of-type(1) > td')[0]
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

            new.text= detail_new.get_text().strip().replace(u'\xa0', '&nbsp;').replace('\n','<br>')



    return new