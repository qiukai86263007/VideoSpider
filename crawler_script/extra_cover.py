import os
import subprocess

def extract_first_frame(input_folder, output_folder):
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.mp4'):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(output_folder, output_filename)
            command = f'ffmpeg -i "{input_path}" -vframes 1 "{output_path}"'
            subprocess.run(command, shell=True)

# 示例用法
input_folder = '/Users/zhangxiaojiang/project/videoproject/crawler_script/video/'
output_folder = '/Users/zhangxiaojiang/project/videoproject/crawler_script/first_frames/'
extract_first_frame(input_folder, output_folder)
