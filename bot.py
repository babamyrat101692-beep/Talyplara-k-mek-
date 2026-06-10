import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8928707476:AAFsPmLTpN_Rb8M9aENMR6LXmRlWBwoXly4"
ADMIN_ID = 5911080183

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salam! TalypKomegi botuna hos geldin!\n\nHyzmatlary:\n\n/referat - Referat\n/doklad - Doklad\n/baha - Bahalar\n/ynanysma - Habarlas")

@dp.message(Command("baha"))
async def baha(message: types.Message):
    await message.answer("Bahalar:\n\nReferat - 300r\nDoklad - 200r\nPrezentasiya - 400r\nMysal - 100r\nKurs isi - 1500r")

@dp.message(Command("referat"))
async def referat(message: types.Message):
    await message.answer("Referat sargyt:\n\n1. Tema:\n2. Sahypa sany:\n3. Hachan gerek:\n\nTolegi: 300r")

@dp.message(Command("ynanysma"))
async def ynanysma(message: types.Message):
    await message.answer("Admin: @Babamyart")

@dp.message()
async def forward_to_admin(message: types.Message):
    await bot.send_message(ADMIN_ID, f"Taze habar!\nAdy: {message.from_user.full_name}\nID: {message.from_user.id}\nHabar: {message.text}")
    await message.answer("Habarunyz alyndy! Admin yakyn wagtda jogap berer.")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
