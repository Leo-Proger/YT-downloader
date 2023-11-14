import glob
import os

from aiogram import Router, F
from aiogram.exceptions import TelegramEntityTooLarge
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from api import download_video_api
from main import bot
from yt_dlp import DownloadError

router = Router()

YOUTUBE_URL_PATTERN = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'


@router.message(Command('start'))
async def greeting(message: Message):
	await message.answer(
		f'Привет, <b>{message.chat.first_name}</b>!\nОтправь мне ссылку на YouTube видео, а я тебе помогу скачать его!',
		parse_mode='HTML'
		)


@router.message(F.text.regexp(YOUTUBE_URL_PATTERN))
async def process_download_video(message: Message, state: FSMContext):
	try:
		await message.answer('Пожалуйста подождите...')

		data = await state.get_data()

		video_info = download_video_api(message.text)

		title, filename, author, duration = (v := video_info)['title'], v['filename'], v['author'], v['duration']

		matches = glob.glob(rf'Z:/videos/{filename}.*')
		if matches:
			video = FSInputFile(matches[0])
			send_text = f'<b>Название</b>: {title}\n<b>Канал</b>: {author}\n<b>Длительность</b>: {duration} секунд(а)'

			await bot.send_video(message.chat.id, video, caption=title)
			await message.answer(send_text, parse_mode='HTML')

			await state.clear()

			os.remove(matches[0])
		else:
			await message.answer('Ошибка. Напишите пожалуйста разработчику [Leo Proger](https://t.me/Leo_Proger)',
			                     parse_mode='MARKDOWN')
	except DownloadError:
		await message.answer('Видео не найдено')
	except TelegramEntityTooLarge as e:
		await message.answer(
			'Видео слишком длинное, я не могу его скачать('
			)


@router.message(F.text)
async def unknown_cmd(message: Message, state: FSMContext):
	await message.answer(
		'Вы можете отправить мне ссылку на видео из YouTube, а я скачаю вам его.\n\n'
		'1.Зайдите на видео, которое хотите скачать\n'
		'2.Найдите кнопку "Поделиться"\n'
		'3.Нажмите кнопку "Скопировать"\n'
		'4.Пришлите мне скопированную ссылку'
		)
