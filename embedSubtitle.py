import subprocess
import os

# Definir las rutas de los directorios y archivos
input_directory = '/Users/chunhaulai/Documents/workspace-personal/video-subtitle-extractor/downloads'
output_directory = '/Users/chunhaulai/Documents/workspace-personal/video-subtitle-extractor/downloads'

# Buscar todos los archivos .mp4 en el directorio de entrada
for file_name in os.listdir(input_directory):
    if file_name.endswith('.mp4'):
        video_file = os.path.join(input_directory, file_name)
        
        # Crear el nombre del archivo .srt_spanish correspondiente
        subtitle_file = os.path.join(input_directory, file_name.replace('.mp4', '.srt_spanish'))
        output_file = os.path.join(output_directory, file_name.replace('.mp4', '_spanish.mp4'))
        
        # Si existe el archivo .srt_spanish, generar el archivo mp4 con los subtítulos incrustados
        if os.path.exists(subtitle_file) and not os.path.exists(output_file):
            subtitle_file_escaped = subtitle_file.replace(" ", "\ ").replace("[", r"\[").replace("]", r"\]")

            # Comando para incrustar subtítulos (usando las rutas originales)
            ffmpeg_command = [
                'ffmpeg',
                '-i', video_file,  # No es necesario escapar aquí
                '-vf', f"subtitles={subtitle_file_escaped}:force_style='Fontsize=35,PrimaryColour=&H03fcff&,OutlineColour=&HFFFFFFFF,BorderStyle=4,BackColour=&H44000000,Outline=6,Shadow=0,MarginV=31'",
                #'-vf', f"subtitles={subtitle_file_escaped}:force_style='BackColour=&HA0000000,BorderStyle=1,Fontsize=35,FontName=Arial,PrimaryColour=&H03fcff&,MarginV=1'",
                '-c:a', 'copy',
                output_file,
            ]
            
            # Ejecutar el comando
            subprocess.run(ffmpeg_command)
            
            print(f'Archivo de video con subtítulos incrustados guardado como {output_file}')
        #else:
        #    print(f'El archivo de subtítulos {subtitle_file} ya existe para el video {video_file}. No es necesario generar un nuevo archivo.')
