from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

class Markups():
    async def start():
        button = InlineKeyboardButton(text='Start', callback_data='startGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def pistol():
        yourself = InlineKeyboardButton(text='Shoot yourself', callback_data='yourself')
        Dealer  = InlineKeyboardButton(text='Shoot the Diller', callback_data='Dealer')
        markup = InlineKeyboardBuilder().add(yourself).row(Dealer).as_markup()
        return markup