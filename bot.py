import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

TOKEN = "8928707476:AAFsPmLTpN_Rb8M9aENMR6LXmRlWBwoXly4"
ADMIN_ID = 5911080183
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_lang = {}
user_pending = {}

async def ask_ai(prompt: str, lang: str = "tk") -> str:
    langs = {
        "tk": "Sen talyplara komek edyan AI. Turkmen dilinde jogap ber. Doly we girisimli jogap ber.",
        "ru": "Ты ИИ-помощник для студентов. Отвечай подробно на русском языке.",
        "en": "You are an AI assistant for students. Reply in detail in English.",
        "ar": "أنت مساعد ذكاء اصطناعي للطلاب. أجب بالتفصيل باللغة العربية."
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": langs.get(lang, langs["tk"])},
                    {"role": "user", "content": prompt}
                ]
            }
        ) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Salam! TalypKomegi botuna hos geldin!\n\n"
        "Dil sayla:\n"
        "/tk - Turkmen\n"
        "/ru - Русский\n"
        "/en - English\n"
        "/ar - عربي\n\n"
        "Hyzmatlary:\n"
        "/referat - Referat (300⭐)\n"
        "/doklad - Doklad (200⭐)\n"
        "/mysal - Mysal (100⭐)\n"
        "/baha - Bahalar"
    )

@dp.message(Command("tk"))
async def lang_tk(message: types.Message):
    user_lang[message.from_user.id] = "tk"
    await message.answer("Turkmen dili saylandi!")

@dp.message(Command("ru"))
async def lang_ru(message: types.Message):
    user_lang[message.from_user.id] = "ru"
    await message.answer("Выбран русский язык!")

@dp.message(Command("en"))
async def lang_en(message: types.Message):
    user_lang[message.from_user.id] = "en"
    await message.answer("English selected!")

@dp.message(Command("ar"))
async def lang_ar(message: types.Message):
    user_lang[message.from_user.id] = "ar"
    await message.answer("تم اختيار العربية!")

@dp.message(Command("baha"))
async def baha(message: types.Message):
    await message.answer("Bahalar:\n\nReferat - 300⭐\nDoklad - 200⭐\nMysal - 100⭐\nKurs isi - 1500⭐")

@dp.message(Command("referat"))
async def referat(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Tema yazin!\nMysal: /referat Ekologiya")
        return
    user_pending[message.from_user.id] = ("referat", args[1])
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Referat",
        description=f"Tema: {args[1]}",
        payload="referat_payment",
        currency="XTR",
        prices=[LabeledPrice(label="Referat", amount=300)]
    )

@dp.message(Command("doklad"))
async def doklad(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Tema yazin!\nMysal: /doklad Fizika")
        return
    user_pending[message.from_user.id] = ("doklad", args[1])
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Doklad",
        description=f"Tema: {args[1]}",
        payload="doklad_payment",
        currency="XTR",
        prices=[LabeledPrice(label="Doklad", amount=200)]
    )

@dp.message(Command("mysal"))
async def mysal(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Mysal yazin!\nMysal: /mysal 2x+5=15")
        return
    user_pending[message.from_user.id] = ("mysal", args[1])
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Mysal",
        description=f"Mysal: {args[1]}",
        payload="mysal_payment",
        currency="XTR",
        prices=[LabeledPrice(label="Mysal", amount=100)]
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    uid = message.from_user.id
    lang = user_lang.get(uid, "tk")
    await message.answer("Toleg alyndy! Yazylyor...")
    
    if uid in user_pending:
        task, tema = user_pending[uid]
        if task == "referat":
            result = await ask_ai(f"Su tema boyunca girisimli referat yaz: {tema}", lang)
        elif task == "doklad":
            result = await ask_ai(f"Su tema boyunca doklad yaz: {tema}", lang)
        elif task == "mysal":
            result = await ask_ai(f"Su mysaly dushundirishli choz: {tema}", lang)
        await message.answer(result[:4000])
        del user_pending[uid]

@dp.message()
async def handle_message(message: types.Message):
    lang = user_lang.get(message.from_user.id, "tk")
    await message.answer("Jogap yazylyor...")
    result = await ask_ai(message.text, lang)
    await message.answer(result[:4000])

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
