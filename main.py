import aiohttp
from vkbottle.bot import Bot, Message
from vkbottle import PhotoMessageUploader
from vkbottle.dispatch.rules.base import AttachmentTypeRule

from dotenv import load_dotenv
import os

load_dotenv()

# Получение токена из переменной окружения
bot_token = os.getenv("BOT_TOKEN")

# Инициализация бота с токеном
bot = Bot(bot_token)

photo_uploader = PhotoMessageUploader(bot.api)

#Функция и декоратор для приветствия пользователя
@bot.on.private_message(text=["Начать", "Здравствуйте", "Привет"])
async def greet_handler(message: Message):
    await message.answer("Привет! Загрузи в меня любое фото и я отправлю его тебе в ответ")

#Функция и декоратор для получения и отправки фото в ответ
@bot.on.message(AttachmentTypeRule("photo"))
async def photo_handler(message: Message):
    photo = message.attachments[0].photo
    largest_photo = max(photo.sizes, key=lambda x: x.width * x.height)
    photo_url = largest_photo.url

    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                image_data = await response.read()
                uploaded_photo = await photo_uploader.upload(file_source=image_data, peer_id=message.peer_id)
                await message.answer(attachment=uploaded_photo)
            else:
                await message.answer("Failed to download the image.")

#Запуск бота
bot.run_forever()
