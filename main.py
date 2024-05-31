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
                        reply_markup=await Markups.start(),
                        link_preview_options=types.LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == 'startGame')
async def startGame(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Game has been started")
    message = callback.message

    blanks  = randint(1, 4)
    live    = randint(1, 4)

    await state.set_state(Game.inGame)
    await state.set_data({
        'blanks':    blanks,
        'live':      live,
        'hpU':       4,
        'hpD':       4
    })

    await message.answer(f"{hbold('Dealer')}: {hbold(blanks)} blanks, {hbold(live)} live ammunition\n"
                        f"Dealer hp: {hbold(4)}, your hp: {hbold(4)}")
    await asyncio.sleep(2)
    await message.answer(f"{hbold('Dealer')}: {hitalic('Gives you a gun')}",
                         reply_markup=await Markups.pistol())

@dp.callback_query(lambda callback: callback.data.startswith('newRound'))
async def newRound(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("New round has been started")
    message = callback.message

    blanks  = randint(1, 4)
    live    = randint(1, 4)
    data    = await state.get_data()
    hpU     = data['hpU']
    hpD     = data['hpD']
    await state.set_data({
        'blanks':    blanks,
        'live':      live,
        'hpU':       hpU,
        'hpD':       hpD
    })

    await message.answer(f"{hbold('Dealer')}: {hbold(blanks)} blanks, {hbold(live)} live ammunition\n"
                        f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}")
    await asyncio.sleep(2)
    if callback.data[-1] == 'U':
        await message.answer(f"{hbold('Dealer')}: {hitalic('Gives you a gun')}",
                            reply_markup=await Markups.pistol())
    else:
        await giveGun(callback, state)

@dp.callback_query(F.data == 'yourself', Game.inGame)
async def yourself(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("You shooted yourself")
    message = callback.message

    data   = await state.get_data()
    blanks = data['blanks']
    live   = data['live']
    hpU    = data['hpU']
    hpD    = data['hpD']
    if blanks != 0 or live != 0:
        if blanks != 0:
            blanks_chanches = round(100 / ((live + blanks) / live))
        else:
            blanks_chanches = 0
        number = randint(0, 100)
        
        if number <= blanks_chanches:
            await state.update_data({
                'blanks': blanks - 1
            })
            await message.answer(f"Blank. You survived\n{hbold(blanks - 1)} blanks, {hbold(live)} live ammunition\n"
                                 f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                                reply_markup=await Markups.pistol())
        else:
            if hpU != 1:
                await state.update_data({
                    'hpU':    hpU - 1
                })
                await message.answer("A live bullet. You lost\n"
                                     f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU - 1)}",
                                    reply_markup=await Markups.newRound('D'))
            else:
                await state.clear()
                await message.answer("A live bullet Game over. Dealer won",
                                    reply_markup=await Markups.again())
    else:
        await state.clear()
        await message.answer("Tie. Out of ammo\n"
                             f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                             reply_markup=await Markups.newRound('U'))

@dp.callback_query(F.data == 'Dealer', Game.inGame)
async def toDealer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("You shooted the Dealer")
    message = callback.message
    
    data   = await state.get_data()
    blanks = data['blanks']
    live   = data['live']
    hpD    = data['hpD']
    hpU    = data['hpU']
    if blanks != 0 or live != 0:
        if blanks != 0:
            blanks_chanches = round(100 / ((live + blanks) / live))
        else:
            blanks_chanches = 0

        number = randint(0, 100)
        
        if number <= blanks_chanches:
            await state.update_data({
                'blanks': blanks - 1
            })
            await message.answer(f"Blank. Dealer survived\n{hbold(blanks - 1)} blanks, {hbold(live)} live ammunition\n"
                                 f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                                reply_markup=await Markups.giveGun())
        else:
            if hpD != 1:
                await state.update_data({
                    'hpD':    hpD - 1
                })
                await message.answer("A live bullet. You won\n"
                                    f"Dealer hp: {hbold(hpD - 1)}, your hp: {hbold(hpU)}",
                                    reply_markup=await Markups.newRound('D'))
            else:
                await state.clear()
                await message.answer("A live bullet. Game over. You won",
                                    reply_markup=await Markups.again())
    else:
        await state.clear()
        await message.answer("Tie. Out of ammo"
                            f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                             reply_markup=await Markups.newRound('U'))

@dp.callback_query(F.data == 'giveGun', Game.inGame)
async def giveGun(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("You gave the gun to Dealer")
    message = callback.message
    
    data   = await state.get_data()
    blanks = data['blanks']
    live   = data['live']
    hpD    = data['hpD']
    hpU    = data['hpU']
    if blanks != 0 or live != 0:
        if blanks != 0:
            blanks_chanches = round(100 / ((live + blanks) / live))
        else:
            blanks_chanches = 0
        number = randint(0, 100)
        is_himself = randint(0, 1) == 0
        if blanks == 0:
            is_himself = False
        # Диллер в себя
        if is_himself:
            await message.answer("Dealer shoots himself.")
            await asyncio.sleep(5)

            if number <= blanks_chanches:
                await state.update_data({
                    'blanks': blanks - 1
                })
                await message.answer(f"Blank. Dealer survived\n{hbold(blanks - 1)} blanks, {hbold(live)} live ammunition\n"
                                     f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                                    reply_markup=await Markups.pistol())
            else:
                if hpD != 1:
                    await state.update_data({
                        'hpD':    hpD - 1
                    })
                    await message.answer("A live bullet. You won\n"
                                        f"Dealer hp: {hbold(hpD - 1)}, your hp: {hbold(hpU)}",
                                    reply_markup=await Markups.newRound('U'))
                else:
                    await state.clear()
                    await message.answer("A live bullet. Game over. You won",
                                        reply_markup=await Markups.again())
        # Диллер в игрока
        else:
            await message.answer("Dealer shoots you.")
            await asyncio.sleep(5)
            if number <= blanks_chanches:
                await state.update_data({
                    'blanks': blanks - 1
                })
                await message.answer(f"Blank. You survived\n{hbold(blanks - 1)} blanks, {hbold(live)} live ammunition\n"
                                     f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU)}",
                                    reply_markup=await Markups.pistol())
            else:
                if hpU != 1:
                    await state.update_data({
                        'hpU':    hpU - 1
                    })
                    await message.answer("A live bullet. You lost\n"
                                        f"Dealer hp: {hbold(hpD)}, your hp: {hbold(hpU - 1)}",
                                    reply_markup=await Markups.newRound('U'))
                else:
                    await state.clear()
                    await message.answer("A live bullet. Game over. Dealer won",
                                        reply_markup=await Markups.again())
    else:
        await state.clear()
        await message.answer("Tie. Out of ammo",
                             reply_markup=await Markups.newRound('D'))

async def main() -> None:
# And the run events dispatching
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())