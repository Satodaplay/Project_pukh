import os
import subprocess
from pytube import extract
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

# Token del bot de Telegram
telegram_token = 'TOKEN'

# Ruta del directorio de destino
destination_dir = "/home/usr/videos/"

# Crear el directorio de destino si no existe
os.makedirs(destination_dir, exist_ok=True)

# Crear una instancia del bot de Telegram
bot = Bot(token=telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Manejador del comando /descargar
@dp.message_handler(Command("audio"))
async def descargar_command(message: types.Message, state: FSMContext):
    # Obtener la URL del video de los argumentos del comando
    video_url = message.get_args()

    # Ejecutar el audio
    filename = extract.video_id(video_url) + ".mp3"
    subprocess.call(["yt-dlp", "-x", "--audio-format", "mp3", "-P", destination_dir, "-o", filename, video_url])

    # Enviar el video al chat especificado
    await bot.send_audio(chat_id=message.chat.id, audio=open(destination_dir + filename, 'rb'))
    os.remove(destination_dir + filename)

# Manejador del comando /descargar
@dp.message_handler(Command("video"))
async def descargar_command(message: types.Message, state: FSMContext):
    # Obtener la URL del video de los argumentos del comando
    video_url = message.get_args()

    # Descargar el video
    filename = extract.video_id(video_url) + ".mp4"
    subprocess.call(["yt-dlp", "--recode-video", "mp4", "-P", destination_dir, "-o", filename, video_url])

    # Enviar el video al chat especificado
    await bot.send_video(chat_id=message.chat.id, video=open(destination_dir + filename, 'rb'))
    os.remove(destination_dir + filename)

# Ejemplo de uso
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
