import logging
import asyncio
import sys
from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.methods.delete_webhook import DeleteWebhook
from aiogram.utils.markdown import hlink, hbold, hitalic
from bot import dp, bot
from keyboards import Markups
from random import randint
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Game(StatesGroup):
    inGame = State()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("It's a Buckshot Roulette game in Telegram!\n"
                        f"Developer: {hlink('mbutsk', 'https://t.me/mbutsk_bot')}",
                        await Markups.start())

@dp.callback_query(F.data == 'startGame')
async def startGame(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Game has been started")
    message = callback.message

    blanks  = randint(1, 4)
    live    = randint(1, 4)

    await state.set_state(Game.inGame)
    await state.set_data({
        'blanks':    blanks,
        'live':      live
    })

    await message.answer(f"{hbold('Dealer')}: {hbold(blanks)} blanks, {hbold(live)} live ammunition")
    await asyncio.sleep(4)
    await message.answer(f"{hbold('Dealer')}: {hitalic('Gives you a gun')}",
                         reply_markup=await Markups.pistol())

@dp.callback_query(F.data == 'startGame')
async def startGame(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("You shooted yourself")
    message = callback.message

    data   = await state.get_data()
    blanks = data['blanks']
    live   = data['live']

    # chanches = 

async def main() -> None:
# And the run events dispatching
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())