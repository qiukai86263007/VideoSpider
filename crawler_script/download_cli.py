import subprocess
import requests
import sys
import os
import logging
import configparser
import fcntl
from multiprocessing import Pool
from crawler_script.common.logging_tools import logger

# Add yt-dlp/yt_dlp directory to sys.path
child_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','yt-dlp'))
sys.path.append(child_project_path)
# 当前目录
current_dir = os.getcwd()
# 设置日志记录

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(current_dir, 'config', 'config.ini'))
proxy_url = config.get('main', 'proxy_url', fallback=None)



# 判断代理能否翻墙
def is_valid_proxy(proxy_url):
    try:
        response = requests.get('https://www.youtube.com/', proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Error validating proxy {proxy_url}: {e}")
        return False

def download_video(url):

    try:
        yt_dlp_dir = os.path.abspath(os.path.join(os.getcwd(), '..','yt-dlp', 'yt_dlp'))
        # Set the arguments for yt-dlp
        sys.argv = [
            '__main__.py',
            '--ffmpeg-location', os.path.join(yt_dlp_dir, 'ffmpeg'),
            '--write-thumbnail',
            '--convert-thumbnails', 'jpg',
            '--merge-output-format', 'mp4',
            '--sleep-subtitles','1' ,
            # '--sleep-requests','1',
            '--sleep-interval','1',
            # '--username', '4684390@qq.com',
            # '--password', 'Qk4684390!',
            '-o', os.path.join(current_dir, '..', 'upload', '%(id)s.%(ext)s'),
            url
        ]
        # If we have proxy_url and accessible, add it to the arguments
        if proxy_url and is_valid_proxy(proxy_url):
            sys.argv.extend(['--proxy', proxy_url])
        logger.info(f"Downloading video from URL: {url}")
        import yt_dlp
        yt_dlp.main()

    except SystemExit as e:
        if e.code == 0:
            logging.info(f"SystemExit occurred: {e}")
            logging.info(f"Successfully downloaded video from URL: {url}")
        else:
            logging.error(f"SystemExit occurred: {e}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error downloading video from URL {url}: {e}")


def main():
    url_file_path = os.path.join(current_dir, 'url.txt')
    if not os.path.exists(url_file_path):
        logging.error(f"URL file not found: {url_file_path}")
        return

    with open(url_file_path, 'r') as file:
        urls = file.readlines()

    with Pool() as pool:
        pool.map(download_video, urls)
        pool.close()  # Close the pool to prevent any more tasks from being submitted
        pool.join()   # Wait for the worker processes to exit
    logger.info("All videos downloaded successfully.")

if __name__ == "__main__":
    lock_file_path = os.path.join(current_dir, 'script.lock')
    with open(lock_file_path, 'w') as lock_file:
        try:
            # Try to acquire an exclusive lock on the file
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            main()
        except IOError:
            logging.error("Another instance of the script is already running.")
            sys.exit(1)
