import os
from openai import OpenAI
from dotenv import load_dotenv
import re

# Cargar variables de entorno
load_dotenv()


# 初始化大模型服务
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = "https://api.fe8.cn/v1",
)


# Definir las rutas de los directorios y archivos
input_directory = '/Users/chunhaulai/Documents/workspace-personal/video-subtitle-extractor/mp4/信'
output_directory = '/Users/chunhaulai/Documents/workspace-personal/video-subtitle-extractor/mp4/信'


# Función para leer el archivo .srt y separar los subtítulos en bloques
def leer_srt(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    # Expresión regular para separar los subtítulos en frames
    frames = re.findall(r"(\d+)\s+([0-9:,.-]+)\s+-->\s+([0-9:,.-]+)\s+(.*?)(?=\n\d+\s|$)", contenido, re.DOTALL)
    return frames


def traducir_subtitulos_lenguaje(texto_concatenado):
    # Definir el mensaje para el modelo
    messages = [
        {
            "role": "user",
            "content": f"""
                有一個srt格式的中文字幕！我須要你把裡面的字幕翻譯成智利國家本地的西班牙文，並保持原來的時間點，不能省略。只提供翻譯後的srt格式字幕，沒有任何解釋、註解或額外文字：
                {texto_concatenado}
            """
        },
    ]
    
    try:
        # Llamada a la API de OpenAI para obtener la traducción
        chat_completion = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=messages
        )
        
        # Verificar si la respuesta contiene el contenido esperado
        if chat_completion.choices and chat_completion.choices[0].message and chat_completion.choices[0].message.content:
            return chat_completion.choices[0].message.content
        else:
            print("Error: La respuesta de la API no contiene contenido válido.")
            return ""  # Retornar cadena vacía si no hay contenido válido en la respuesta

    except Exception as e:
        print(f"Error en la traducción: {e}")
        return ""  # Retornar cadena vacía en caso de error



# Función para traducir los subtítulos
def traducir_subtitulos(frames):
    frames_traducidos = ""
    
    # Traducir en bloques de 80 frames
    for i in range(0, len(frames), 40):
        texto_concatenado = ""  # Reiniciar texto_concatenado por cada bloque
        bloque = frames[i:i+40]
        
        for frame in bloque:
            texto_concatenado = f"{texto_concatenado}\n{frame[0]}\n{frame[1]} --> {frame[2]}\n{frame[3]}" 
        
        # Aquí puedes hacer algo con `texto_concatenado` para cada bloque (por ejemplo, traducirlo o imprimirlo)
        #print(texto_concatenado)  # O el procesamiento que desees hacer
        frames_traducidos = frames_traducidos + "\n" + traducir_subtitulos_lenguaje(texto_concatenado)
        print(frames_traducidos)
    return frames_traducidos



# Función para guardar el archivo traducido
def guardar_srt_traducido(frames_traducidos, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.write(frames_traducidos)

# Buscar todos los archivos .srt en el directorio de entrada
for file_name in os.listdir(input_directory):
    if file_name.endswith('.mp4'):
        srt_file = os.path.join(input_directory, file_name.replace('.mp4', '.srt'))
        subtitle_file = os.path.join(input_directory, file_name.replace('.mp4', '_spanish.srt'))
        if not os.path.exists(subtitle_file):
            frames = leer_srt(srt_file)
            frames_traducidos = traducir_subtitulos(frames)
            guardar_srt_traducido(frames_traducidos, subtitle_file)
            # Procesar el archivo de subtítulos
            print(f"Subtítulos traducidos guardados en: {subtitle_file}")
