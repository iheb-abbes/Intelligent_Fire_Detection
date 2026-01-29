import cv2
import yt_dlp
import os

def get_video_stream(source):
    """
    Module 4.1: Supporte les fichiers locaux et les sources YouTube.
    Utilise Deno pour contourner les restrictions de signature JS.
    """
    if "youtube.com" in source or "youtu.be" in source:
        # Configuration optimisée pour yt-dlp avec Deno
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            # On force l'utilisation de Deno comme runtime JavaScript
            'js_runtime': 'deno',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"DEBUG: Extraction du flux via Deno pour {source}...")
                info = ydl.extract_info(source, download=False)
                # Le lien direct vers le flux vidéo
                return info['url']
        except Exception as e:
            print(f"ERREUR d'extraction YouTube : {e}")
            return None
            
    return source

def process_frame(frame, width=640, height=480):
    """
    Ajuste la résolution pour équilibrer temps de détection et précision.
    """
    if frame is None:
        return None
    return cv2.resize(frame, (width, height))