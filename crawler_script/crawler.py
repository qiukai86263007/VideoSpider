# https://www.apnews.com/
import requests
import json

# 定义搜索接口URL
search_url = "https://www.apnews.com/apf-video/top-headlines"

# 发送HTTP请求获取搜索结果
response = requests.get(search_url)

# 检查响应状态码
if response.status_code == 200:
    # 解析JSON数据
    data = response.json()

    # 提取视频URL
    video_urls = []
    for item in data['results']:
        if 'video' in item and 'url' in item['video']:
            video_urls.append(item['video']['url'])

    # 打印视频URL
    for url in video_urls:
        print(url)
else:
    print("Failed to retrieve data from AP News.")