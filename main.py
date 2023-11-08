import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from aiogram.types import Message
from yt_dlp import DownloadError

from api import download_video_api
from config_reader import config

bot = Bot(token=config.TOKEN.get_secret_value(), parse_mode='html')
dp = Dispatcher()


@dp.message(Command('start'))
async def greeting(message: Message):
	await message.answer(
		f'Привет, <b>{message.chat.first_name}</b>!\nОтправь мне ссылку на YouTube видео, а я тебе помогу скачать его!',
		parse_mode='HTML')


@dp.message(F.text)
async def download_video(message: Message):
	try:
		await message.answer('Пожалуйста подождите...')
		video_info = download_video_api(message.text)

		title = video_info['title']
		filename = video_info['filename']
		author = video_info['author']
		duration = video_info['duration']
		print(title)

		video = FSInputFile(rf'Z:\videos\{filename}.mp4')
		await bot.send_video(message.chat.id, video, caption=title)

		send_text = f'<b>Название</b>: {title}\n<b>Канал</b>: {author}\n<b>Длительность</b>: {duration} секунд'
		await message.answer(send_text, parse_mode='HTML')

	except DownloadError as e:
		await message.answer('Видео не найдено или ссылка неправильно введена')


async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')
