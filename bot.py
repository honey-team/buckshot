from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

# Подключение бота к АПИ
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
