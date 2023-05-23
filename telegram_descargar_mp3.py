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

# Nombre del archivo de audio
audio_file = "audio.mp3"

# Ruta completa del directorio de destino
destination_path = os.path.join(destination_dir, video_file)

# Crear el directorio de destino si no existe
os.makedirs(destination_dir, exist_ok=True)

# Crear una instancia del bot de Telegram
bot = Bot(token=telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Función para descargar y enviar el video en formato MP3 por Telegram
async def descargar_y_enviar_video(video_url, chat_id):
    # Crear una instancia de la clase YouTube con la URL del video
    yt = YouTube(video_url)

    # Obtener el objeto de audio disponible
    audio = yt.streams.filter(only_audio=True).first()

    # Descargar el audio en la ruta de destino especificada
    audio.download(output_path=destination_dir, filename=audio_file)

    # Ruta completa del archivo de audio
    audio_path = os.path.join(destination_dir, audio_file)

    # Comando para convertir el archivo de audio a MP3
    convert_command = f"ffmpeg -i {audio_path} {audio_path[:-4]}.mp3"

    # Ejecutar el comando de conversión
    subprocess.run(convert_command, shell=True)

    # Ruta completa del archivo de audio convertido a MP3
    mp3_path = f"{audio_path[:-4]}.mp3"

    # Enviar el archivo de audio al chat especificado
    await bot.send_audio(chat_id=chat_id, audio=open(mp3_path, 'rb'))

    # Comando Bash que deseas ejecutar
    bash_command = "bash /home/usuario/borrar_video.sh"

    # Ejecutar el comando Bash
    subprocess.run(bash_command, shell=True)

# Manejador del comando /descargar
@dp.message_handler(Command("audio"))
async def descargar_command(message: types.Message, state: FSMContext):
    # Obtener la URL del video de los argumentos del comando
    video_url = message.get_args()

    # ID del chat de Telegram al que se enviará el video descargado
    chat_id = message.chat.id

    # Llamar a la función para descargar y enviar el video en formato MP3
    await descargar_y_enviar_video(video_url, chat_id)

# Ejemplo de uso
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
