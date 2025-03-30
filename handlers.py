from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from utils import analyze_mood_with_openai, send_amplitude_event
import base64
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Отправьте фото лица для анализа настроения!")

@router.message(F.photo)
async def photo_handler(message: Message):
    user_id = message.from_user.id
    
    try:
        # Получаем файл фото
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        
        # Скачиваем файл
        image_data = await message.bot.download_file(file.file_path)
        
        # Читаем содержимое файла и кодируем
        image_bytes = image_data.getvalue()  # Используем getvalue() для BytesIO
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Проверка минимального размера
        if len(base64_image) < 1000:
            await message.answer("Фото слишком маленького размера")
            return

        # Анализ настроения
        mood = await analyze_mood_with_openai(base64_image)
        response = f"🔍 Ваше настроение: {mood.capitalize()}"
        
        await message.answer(response)
        send_amplitude_event("mood_analyzed", user_id, {"mood": mood})

    except Exception as e:
        logger.error(f"Photo processing error: {str(e)}")
        await message.answer("⚠️ Не удалось проанализировать фото. Попробуйте другое изображение.")