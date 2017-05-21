#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import json
from hello import db,Videos
def test():
    base_url='http://neihanshequ.com/video/'
    url='http://neihanshequ.com/video/?is_json=1&app_name=neihanshequ_web&max_time='
    req_text=requests.get(base_url).text
    soup = BeautifulSoup(req_text, "html.parser")
    videos=soup.select('#detail-list > li')
    for video in videos:
        vedio_digg_count = int(video.select('div > div.options > ul > li.digg-wrapper > span')[0].string)
        if (vedio_digg_count < 10000):
            continue
        video_description=video.select('div > div.content-wrapper > a > div > h1 > p')[0].string
        video_img=video.select('#videoContainer > div.player-container')[0]['data-poster-src']
        video_url=video.select('#videoContainer > div.player-container')[0]['data-src']

        vdo=Videos(vedio_digg_count=vedio_digg_count,video_description=video_description,video_img=video_img,video_url=video_url)
        db.session.add(vdo)
        db.session.commit()


    max_time=re.search(r'max_time: \'(\d+)\'', req_text).group(1)
    while(max_time):
        text = requests.get(url+max_time).text
        data= json.loads(text)
        max_time= data['data']['min_time']
        for da in data['data']['data']:
            vedio_digg_count = da['group']['digg_count']
            if (vedio_digg_count<10000):
                continue
            video_url= da['group']['origin_video']['url_list'][0]['url']
            if (Videos.query.filter_by(video_url=video_url).first()):
                continue
            video_img= da['group']['medium_cover']['url_list'][0]['url']
            video_description= da['group']['text']

            vdo = Videos(vedio_digg_count=vedio_digg_count, video_description=video_description, video_img=video_img,
                         video_url=video_url)
            db.session.add(vdo)
            db.session.commit()

        break



test()