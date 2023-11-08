import os
import re

from yt_dlp import YoutubeDL
from typing import Literal

VIDEO_FORMATS = {
	'normal': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
	'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
	}


# TODO: Удалять файлы через некоторое время
def delete_file(filename):
	if os.path.exists(filename):
		os.remove(filename)


def extract_video_id(url):
	video_id = re.search(r'(?<=v=)[^&#]+', url)
	if video_id:
		return video_id.group(0)
	else:
		video_id = re.search(r'(?<=v=)[^&]+', url)
		return video_id.group(0) if video_id else None


# TODO: Сделать асинхронным
def download_video_api(url: str, quality: Literal['normal', 'best'] = 'normal') -> dict:
	filename = extract_video_id(url)

	ydl_opts: dict = {
		'format': VIDEO_FORMATS[quality],
		'outtmpl': f'Z:/videos/{filename}.mp4',
		'noplaylist': True,
		}

	with YoutubeDL(ydl_opts) as ydl:
		info_dict = ydl.extract_info(url, download=False)

		ydl.download([url])

		video_info = {
			'title': info_dict.get('title', 'No title'),
			'filename': filename,
			'author': info_dict.get('uploader', 'No author'),
			'duration': info_dict.get('duration', 'No duration'),
			}

		return video_info

# print(download_video_api('https://youtu.be/l-sTQBr3rXY?si=b02a1bHIHmJ9s0fm'))
