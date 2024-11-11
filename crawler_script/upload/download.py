import os.path
import subprocess


def download(video_id, path, type='yt'):
    """
    yt-dlp下载器
    """
    if os.path.exists(path):
        print(f'视频文件已存在，{video_id}')
        return
    if type == 'yt':
        url = f"https://youtu.be/{video_id}"
        print("视频下载，subprocess：", ['yt-dlp', '-o', path, '-f', '22', url])
        subprocess.run(['yt-dlp', '-o', path, '-f', '22', url])


def get_cover_from_video(video, cover_path):
    """
    从mp4文件拆帧，生成封面图片
    """
    if os.path.exists(cover_path):
        print(f'封面图像已存在，{cover_path}')
        return
    command = f'ffmpeg -i "{video}" -vframes 1 "{cover_path}"'
    print("视频封面拆帧，subprocess：", command)
    subprocess.run(command, shell=True)
