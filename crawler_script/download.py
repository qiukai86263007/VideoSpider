import subprocess

import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/zhangxiaojiang/Desktop/video/Runs dataset 2024-03-16_副本.csv')

# 过滤channelName列中值不等于"王志安"的行
filtered_df = df[df['channelName'] != '王志安']

# 提取每一行中的id值，拼接成新的url，并打印出来
for index, row in filtered_df.iterrows():
    video_id = row['id']
    url = f"https://youtu.be/{video_id}"
    # 指定下载目录并设置并发度为5
    subprocess.run(
        ['yt-dlp', '-o', '/Users/zhangxiaojiang/project/videoproject/crawler_script/video/%(title)s.%(ext)s', '-f', '22', url])

