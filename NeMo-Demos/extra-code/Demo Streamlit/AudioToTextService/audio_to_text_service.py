import requests
import json
import numpy as np
from pydub import AudioSegment
import os
import speech_recognition as sr
from urllib3.exceptions import InsecureRequestWarning
import warnings
import base64
import logging


logging.basicConfig(level=logging.INFO)

class AudioToTextService:
    def __init__(self, model_service_url):
        self.model_service_url = model_service_url
        self.recognizer = sr.Recognizer()
        logging.info("AudioToTextService initialized with model service URL: %s", model_service_url)

    def convert_mp3_to_wav(self, mp3_path):
        temp_wav_path = os.path.splitext(mp3_path)[0] + "_temp.wav"
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(temp_wav_path, format="wav")
        logging.info("Converted MP3 to WAV: %s", temp_wav_path)
        return temp_wav_path

    def mp3_to_text(self, mp3_path):
        wav_path = self.convert_mp3_to_wav(mp3_path)
        with sr.AudioFile(wav_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data)
                logging.info("Text from audio: %s", text)
            except sr.UnknownValueError:
                text = "Não foi possível entender o áudio"
                logging.warning(text)
            except sr.RequestError as e:
                text = f"Erro de solicitação do serviço de reconhecimento de voz; {e}"
                logging.error(text)
        
        os.remove(wav_path)
        return text
    
    def send_audio_for_translation(self, mp3_path):

        converted_text = self.mp3_to_text(mp3_path)

        wav_path = self.convert_mp3_to_wav(mp3_path)
        with open(wav_path, 'rb') as f:
            audio_bytes = f.read()
        os.remove(wav_path)
        
        encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')
        
        request_body = {
            "inputs": {
                "source_serialized_audio": [encoded_audio],
                "source_text": [converted_text]  
            },
            "params":{
                "use_audio": True
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.model_service_url + "/invocations", headers=headers, json=request_body, verify=False)
        
        if response.status_code == 200:
            logging.info("Successful response from model service")
            return response.json()
        else:
            logging.error("Failed request to model service. Status Code: %s, Response Text: %s", response.status_code, response.text)
            return {"error": "Falha na solicitação para o serviço do modelo", "status_code": response.status_code, "message": response.text}


