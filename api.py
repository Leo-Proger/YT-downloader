import os

from yt_dlp import YoutubeDL


# TODO: Удалять файлы через некоторое время
def delete_file(filename):
	if os.path.exists(filename):
		os.remove(filename)


# TODO: Сделать асинхронным; заменять символы, который не поддерживает windows
def download_video_api(url: str) -> dict:
	ydl_opts: dict = {
		'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
		'outtmpl': 'Z:/videos/%(title)s.%(ext)s',
		}

	with YoutubeDL(ydl_opts) as ydl:
		info_dict = ydl.extract_info(url, download=False)

		video_info = {
			'title': info_dict.get('title', 'No title'),
			'author': info_dict.get('uploader', 'No author'),
			'duration': info_dict.get('duration', 'No duration'),
			}
		ydl.download([url])
		return video_info
