import os
import asyncio
import subprocess
from pytube import YouTube
from telegram import Bot

# Token del bot de Telegram
telegram_token = ' '

# Función asincrónica para descargar el video y enviarlo por Telegram
async def descargar_y_enviar_video(video_url, chat_id):
    # Ruta del directorio de destino
    destination_dir = "/home/usuario/videos/"

    # Nombre del archivo de video
    video_file = "video.mp4"

    # Ruta completa del directorio de destino
    destination_path = os.path.join(destination_dir, video_file)

    # Crear el directorio de destino si no existe
    os.makedirs(destination_dir, exist_ok=True)

    # Crear una instancia de la clase YouTube con la URL del video
    yt = YouTube(video_url)

    # Obtener la mejor resolución disponible
    stream = yt.streams.get_highest_resolution()

    # Descargar el video en la ruta de destino especificada
    stream.download(output_path=destination_dir, filename=video_file)

    # Crear una instancia del bot de Telegram
    bot = Bot(token=telegram_token)

    # Enviar el video al chat especificado
    await bot.send_video(chat_id=chat_id, video=open(destination_path, 'rb'))

    # Comando Bash que deseas ejecutar
    bash_command = "bash /home/usuario/borrar_video.sh"

    # Ejecutar el comando Bash
    subprocess.run(bash_command, shell=True)

# Ejemplo de uso
async def main():
    # URL del video de YouTube que deseas descargar
    video_url = "https://www.youtube.com/YOUTUBEID"

    # ID del chat de Telegram al que se enviará el video descargado
    chat_id = ' '

    # Llamar a la función asincrónica para descargar y enviar el video
    await descargar_y_enviar_video(video_url, chat_id)

if __name__ == '__main__':
    asyncio.run(main())
