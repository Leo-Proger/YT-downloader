import asyncio

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import download_video

bot = Bot(token=config.TOKEN.get_secret_value(), parse_mode='html')


async def main():
	dp = Dispatcher()

	dp.include_router(download_video.router)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot, polling_timeout=300)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')
