import glob

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from api import download_video_api
from keyboards.for_questions import quality_choice_kb
from main import bot
from yt_dlp import DownloadError

router = Router()

YOUTUBE_URL_PATTERN = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'


class Form(StatesGroup):
	url = State()
	quality = State()


@router.message(Form.quality)
async def process_download_video(message: Message, state: FSMContext) -> None | str:
	try:
		await state.update_data(quality=message.text)
		print(await state.get_state())

		await message.answer('Пожалуйста подождите...')

		data = await state.get_data()
		url = data['url']
		quality = data['quality']

		video_info = download_video_api(url, quality)

		title = video_info['title']
		filename = video_info['filename']
		author = video_info['author']
		duration = video_info['duration']

		matches = glob.glob(rf'Z:/videos/{filename}.*')
		if matches:
			video = FSInputFile(matches[0])
			send_text = f'<b>Название</b>: {title}\n<b>Канал</b>: {author}\n<b>Длительность</b>: {duration} секунд'

			await bot.send_video(message.chat.id, video, caption=title)
			await message.answer(send_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')

			await state.clear()
	except DownloadError as e:
		await message.answer('Видео не найдено', reply_markup=ReplyKeyboardRemove())


@router.message(Command('start'))
async def greeting(message: Message):
	await message.answer(
		f'Привет, <b>{message.chat.first_name}</b>!\nОтправь мне ссылку на YouTube видео, а я тебе помогу скачать его!',
		parse_mode='HTML')


@router.message(F.text.regexp(YOUTUBE_URL_PATTERN))
async def process_quality_choice(message: Message, state: FSMContext):
	await state.update_data(url=message.text)
	await state.set_state(Form.quality)

	data = await state.get_data()
	print(data.get('url'))

	keyboard = quality_choice_kb()

	await message.answer('Выберите качество видео', reply_markup=keyboard)


@router.message(F.text)
async def unknown_cmd(message: Message, state: FSMContext):
	await message.answer(
		'Вы можете отправить мне ссылку на видео из YouTube, а я скачаю вам его.\n\n'
		'1.Зайдите на видео, которое хотите скачать\n'
		'2.Найдите кнопку поделиться\n'
		'3.Нажмите кнопку "Скопировать"\n'
		'4.Пришлите мне скопированную ссылку'
		)
