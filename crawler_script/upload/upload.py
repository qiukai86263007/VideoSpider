import os.path

import pandas as pd

from crawler_script.upload.download import download, get_cover_from_video
from crawler_script.upload.mysql_tools import set_classification, upload_video

df = pd.read_excel("/Users/zhangxiaojiang/Desktop/video/video.xlsx")

df = df[df['channelName'].notna()]
print(df)
# 服务器视频文件目录
server_video_file_directory = "/Users/zhangxiaojiang/project/videoproject/upload"
# 服务器视频封面目录
server_cover_file_directory = "/Users/zhangxiaojiang/project/videoproject/upload/cover"

# 提取每一行中的id值，拼接成新的url，并打印出来
for index, row in df.iterrows():
    video_id = row['id']
    title = row['title']
    desc = row['text']
    channel_Name = row['channelName']
    video_path = os.path.join(server_video_file_directory, video_id + '.mp4')
    cover_path = os.path.join(server_cover_file_directory, video_id + '.jpg')
    # 下载视频
    download(video_id, video_path)
    # 抽取封面
    get_cover_from_video(video_path, cover_path)
    # 视频分类信息更新，获取分类id
    classification_id = set_classification(channel_Name)
    # 视频数据库信息更新
    upload_video(title, desc, classification_id, os.path.basename(video_path), "cover/"+os.path.basename(cover_path))
    print('---'*10+'上传成功'+'---'*10)
    print(f'title:{title}\n, channel_Name:{channel_Name}')
