from shutil import which

import speech_recognition as sr
from pydub import AudioSegment
from langdetect import detect
import os

AudioSegment.ffmpeg = which("ffmpeg")

from pydub import AudioSegment
from pydub.utils import which

# Asegúrate de que ffmpeg esté en el PATH
AudioSegment.ffmpeg = which("ffmpeg")

def convert_to_wav(input_file):
    try:
        # Cargar el archivo de audio sin usar mimetypes
        audio = AudioSegment.from_file(input_file)

        # Definir el archivo de salida
        output_file = f"audios/audio_converted.wav"

        # Exportamos el audio a formato WAV
        audio.export(output_file, format="wav")
        print(f"Archivo convertido a {output_file}")
        return output_file

    except Exception as e:
        print(f"Error al convertir el archivo {input_file}: {e}")
        return None


def detect_language(text):
    try:
        # Detecta el idioma del texto
        language = detect(text)
        print(f"El idioma detectado es: {language}")
        return language
    except Exception as e:
        print(f"Error al detectar el idioma: {e}")
        return None


def recognize_speech(input_file):
    wav_file = convert_to_wav(input_file)

    if wav_file:
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(wav_file) as source:
                print("Preparando el audio...")
                audio = recognizer.record(source)  # Leemos todo el audio

            languages_to_try = ['es-ES', 'en-US', 'fr-FR', 'de-DE', 'it-IT', 'pt-BR']
            recognized_text = ""

            for lang in languages_to_try:
                try:
                    recognized_text = recognizer.recognize_google(audio, language=lang)
                    print(f"Texto reconocido en {lang}: {recognized_text}")
                    break
                except sr.UnknownValueError:
                    print(f"No se pudo reconocer el audio en {lang}. Intentando otro idioma.")
                except sr.RequestError:
                    print(f"Error de solicitud con el idioma {lang}.")

            if recognized_text:
                detect_language(recognized_text)
                return recognized_text
            else:
                return "No se pudo reconocer el audio en ninguno de los idiomas intentados."

        except Exception as e:
            print(f"Error durante el reconocimiento: {e}")
            return ""
        finally:
            if os.path.exists(wav_file):
                os.remove(wav_file)
                os.remove(input_file)
                print("Archivo WAV temporal eliminado.")
    else:
        return ""

# convert_to_wav("51949638354_20241117_213802.mpeg")
print(recognize_speech("51949638354_20241117_213802.mpeg"))