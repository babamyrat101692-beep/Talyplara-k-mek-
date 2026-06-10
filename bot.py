import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8928707476:AAFsPmLTpN_Rb8M9aENMR6LXmRlWBwoXly4"
ADMIN_ID = 5911080183
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def ask_ai(prompt: str, lang: str = "tk") -> str:
    if lang == "tk":
        system = "Sen talyplara kömek edyan AI. Türkmen dilinde jogap ber."
    elif lang == "ru":
        system = "Ты ИИ-помощник для студентов. Отвечай на русском языке."
    elif lang == "en":
        system = "You are an AI assistant for students. Reply in English."
    elif lang == "ar":
        system = "أنت مساعد ذكاء اصطناعي للطلاب. أجب باللغة العربية."
    else:
        system = "Sen talyplara kömek edyan AI."

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": system},
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
        "Dil sayla / Выберите язык:\n\n"
        "/tk - Turkmen\n"
        "/ru - Русский\n"
        "/en - English\n"
        "/ar - عربي"
    )

@dp.message(Command("tk"))
async def lang_tk(message: types.Message):
    await message.answer("Turkmen dili saylandi! Soragiizi yazin:")

@dp.message(Command("ru"))
async def lang_ru(message: types.Message):
    await message.answer("Выбран русский язык! Напишите ваш вопрос:")

@dp.message(Command("en"))
async def lang_en(message: types.Message):
    await message.answer("English selected! Write your question:")

@dp.message(Command("ar"))
async def lang_ar(message: types.Message):
    await message.answer("تم اختيار العربية! اكتب سؤالك:")

@dp.message(Command("referat"))
async def referat(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Tema yazin! Mysal: /referat Ekologiya")
        return
    await message.answer("Referat yazylyor, garasyn...")
    result = await ask_ai(f"Su tema boyunca 10 sahypalyk referat yaz: {args[1]}")
    await message.answer(result[:4000])

@dp.message(Command("mysal"))
async def mysal(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Mysal yazin! Mysal: /mysal 2+2*3")
        return
    await message.answer("Mysal chozulyor...")
    result = await ask_ai(f"Su mysaly choz we dushundir: {args[1]}")
    await message.answer(result[:4000])

@dp.message(Command("baha"))
async def baha(message: types.Message):
    await message.answer(
        "Bahalar:\n\nReferat - 300r\nDoklad - 200r\nMysal - 100r\nKurs isi - 1500r"
    )

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("Jogap yazylyor...")
    result = await ask_ai(message.text)
    await message.answer(result[:4000])

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
