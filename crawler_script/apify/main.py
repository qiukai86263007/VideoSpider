import json
import os
from tool import craw_web,craw_web_vedio,craw_ytb_vedio
from web import web_list
os.environ['APIFY_API_TOKEN'] = 'apify_api_gRoYxg0iiL3qd8bMANtcWFQUkgP0bA1qFTcK'


# 爬取传统媒体
news_sources = web_list.split('\n')
q = ''
for web in news_sources:
    q+= f'''"Wang Zhi'an" OR "Wang Zhian" OR "王志安" OR "王局志安" site:{web.strip()}\n'''
craw_web_vedio(q)


# 爬取 ytb
craw_ytb_vedio("Wang Zhi'an 王志安 Wang Zhian",10)