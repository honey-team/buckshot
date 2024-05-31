from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

class Markups():
    async def start():
        button = InlineKeyboardButton(text='Start', callback_data='startGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def pistol():
        yourself = InlineKeyboardButton(text='Shoot yourself', callback_data='yourself')
        Dealer  = InlineKeyboardButton(text='Shoot the Dealer', callback_data='Dealer')
        markup = InlineKeyboardBuilder().add(yourself).row(Dealer).as_markup()
        return markup
    
    async def again():
        button = InlineKeyboardButton(text='Play again', callback_data='startGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def giveGun():
        button = InlineKeyboardButton(text='Give the gun to the Dealer', callback_data='giveGun')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup