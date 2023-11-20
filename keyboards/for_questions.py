from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def quality_choice_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardBuilder()
	kb.button(text='До 1080p')
	kb.button(text='Лучшее')

	# Означает, что во всех строках будет по 1 кнопке
	kb.adjust(1)

	return kb.as_markup(resize_keyboard=True)
