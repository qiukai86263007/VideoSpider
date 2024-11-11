import os.path
import time

import pandas as pd

from upload.download import download, get_cover_from_video
from upload.mysql_tools import set_classification, upload_video
import emoji
import os
from apify.tool import craw_web,craw_web_vedio,craw_ytb_vedio
from apify.web import web_list
import re
os.environ['APIFY_API_TOKEN'] = 'apify_api_gRoYxg0iiL3qd8bMANtcWFQUkgP0bA1qFTcK'

def remove_non_ascii(text):
    return emoji.replace_emoji(text, replace='')

# 爬取传统媒体
news_sources = web_list.split('\n')
q = ''
for web in news_sources:
    q+= f'''"Wang Zhi'an" OR "Wang Zhian" OR "王志安" OR "王局志安" site:{web.strip()}\n'''
# craw_web_vedio(q)


# 爬取wm
video_info = craw_ytb_vedio("Wang Zhi'an 王志安 Wang Zhian",10)
# df = pd.read_excel("/Users/zhangxiaojiang/Desktop/video/video.xlsx")
print("---"*10+"video_info"+"---"*10)
for video in video_info:
    print("---"*10)
    video_id = video['id']
    title = video['title']
    desc = video['text']
    print(f'title:{title}\n, desc:{desc}, video_id:{video_id}')
    time.sleep(1)
# df = df[df['channelName'].notna()]
# print(df)
# 服务器视频文件目录
server_video_file_directory = "/Users/zhangxiaojiang/project/videoproject/upload"
# 服务器视频封面目录
server_cover_file_directory = "/Users/zhangxiaojiang/project/videoproject/upload/cover"
print("---"*10+"start download & upload"+"---"*10)
for video in video_info:
    video_id = video['id']
    title = video['title']
    desc = video['text']
    channel_Name = video['channel']
    video_path = os.path.join(server_video_file_directory, video_id + '.mp4')
    cover_path = os.path.join(server_cover_file_directory, video_id + '.jpg')
    # 下载视频
    # download(video_id, video_path)
    # 抽取封面
    # get_cover_from_video(video_path, cover_path)
    # 视频分类信息更新，获取分类id
    # classification_id = set_classification(channel_Name)
    # 视频数据库信息更新
    # upload_video(remove_non_ascii(title), remove_non_ascii(desc), classification_id, os.path.basename(video_path), "cover/"+os.path.basename(cover_path))
    print('---'*10+'上传成功'+'---'*10)
    print(f'title:{title}\n, channel_Name:{channel_Name}')
    break
