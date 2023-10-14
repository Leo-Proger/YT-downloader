import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile, URLInputFile

from config_reader import config

bot = Bot(token=config.TOKEN.get_secret_value(), parse_mode='html')
dp = Dispatcher()


@dp.message(Command('name'))
async def cmd_start(message: Message, command: CommandObject):
	if a := command.args:
		await message.answer(f'<b>Привет! {a}</b>')
	else:
		await message.answer('Введи свое имя')


@dp.message(F.text)
async def receiving_text(message: Message):
	if message.text == 'get_img':
		result_image = None
		images = [r'C:\Users\Leonid\Pictures\Космос0.jpg',
		          'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRD_gTG_W0gNIGyWkhFq-ifMlFkAA9rb3RoJ8Uz1BaI&s']
		random_image = images[random.randint(0, 1)]
		try:
			result_image = FSInputFile(random_image)
		except:
			result_image = URLInputFile(random_image)
		result = await message.answer_photo(
			result_image,
			caption='Test image'
			)
		print(result.photo[-1].file_id)


# else:
# 	data = {
# 		'url': '',
# 		'email': '',
# 		'code': ''
# 		}
#
# 	entities = message.entities or []
#
# 	for item in entities:
# 		if item.type in data.keys():
# 			data[item.type] = item.extract_from(message.text)
# 	await message.reply(f'Вот что я нашел: {html.quote(data[0])}')


async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')
