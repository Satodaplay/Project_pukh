from pytube import YouTube

# URL del video de YouTube que deseas descargar
video_url = "https://www.youtube.com/YOUTUBEID"

# Ruta de destino donde se guardará el video descargado
save_path = "/home/usuario/videos/video.mp4"

# Crear una instancia de la clase YouTube con la URL del video
yt = YouTube(video_url)

# Obtener la mejor resolución disponible
stream = yt.streams.get_highest_resolution()

# Descargar el video en la ruta de destino especificada
stream.download(output_path=save_path)

print("¡Descarga completa!")
