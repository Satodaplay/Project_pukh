import os
import asyncio
import subprocess
from pytube import YouTube
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

# Token del bot de Telegram
telegram_token = ' '

# Ruta del directorio de destino
destination_dir = "/home/usuario/videos/"

# Nombre del archivo de video
video_file = "video.mp4"

# Ruta completa del directorio de destino
destination_path = os.path.join(destination_dir, video_file)

# Crear el directorio de destino si no existe
os.makedirs(destination_dir, exist_ok=True)

# Crear una instancia del bot de Telegram
bot = Bot(token=telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Función para descargar y enviar el video por Telegram
async def descargar_y_enviar_video(video_url, chat_id):
    # Crear una instancia de la clase YouTube con la URL del video
    yt = YouTube(video_url)

    # Obtener la mejor resolución disponible
    stream = yt.streams.get_highest_resolution()

    # Descargar el video en la ruta de destino especificada
    stream.download(output_path=destination_dir, filename=video_file)

    # Enviar el video al chat especificado
    await bot.send_video(chat_id=chat_id, video=open(destination_path, 'rb'))

    # Comando Bash que deseas ejecutar
    bash_command = "bash /home/usuario/borrar_video.sh"

    # Ejecutar el comando Bash
    subprocess.run(bash_command, shell=True)

# Manejador del comando /descargar
@dp.message_handler(Command("video"))
async def descargar_command(message: types.Message, state: FSMContext):
    # Obtener la URL del video de los argumentos del comando
    video_url = message.get_args()

    # ID del chat de Telegram al que se enviará el video descargado
    chat_id = message.chat.id

    # Llamar a la función para descargar y enviar el video
    await descargar_y_enviar_video(video_url, chat_id)

# Ejemplo de uso
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)