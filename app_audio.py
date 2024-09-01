import streamlit as st
from io import BytesIO
from pathlib import Path
import speech_recognition as sr
from playsound import playsound
import openai
from dotenv import load_dotenv, find_dotenv

# Carregue as variáveis de ambiente
load_dotenv(find_dotenv())

api_key = 'sk-proj-89krMLQUsp9delCCbqZ2T3BlbkFJaJdzrpaTrqQqvzryLN0b'
openai.api_key = api_key

ARQUIVO_AUDIO = 'fala_assistant.mp3'
recognizer = sr.Recognizer()

def grava_audio():
    with sr.Microphone() as source:
        st.write('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio(audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'
    transcricao = openai.Audio.transcribe(
        model='whisper-1',
        file=wav_data,
    )
    return transcricao['text']

def completa_texto(mensagens):
    resposta = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=mensagens,
        max_tokens=1000,
        temperature=0
    )
    return resposta

def cria_audio(texto):
    if Path(ARQUIVO_AUDIO).exists():
        Path(ARQUIVO_AUDIO).unlink()
    resposta = openai.Audio.create(
        model='tts-1',
        voice='shimmer',
        input=texto
    )
    with open(ARQUIVO_AUDIO, 'wb') as f:
        f.write(resposta['data'])
    return ARQUIVO_AUDIO

st.title("Aplicativo de Reconhecimento de Voz e ChatGPT")

mensagens = []

if st.button("Gravar áudio"):
    audio = grava_audio()
    transcricao = transcricao_audio(audio)
    mensagens.append({'role': 'user', 'content': transcricao})
    st.write(f'User: {mensagens[-1]["content"]}')
    resposta = completa_texto(mensagens)
    mensagens.append({'role': 'assistant', 'content': resposta['choices'][0]['message']['content']})
    st.write(f'Assistant: {mensagens[-1]["content"]}')
    audio_file = cria_audio(mensagens[-1]["content"])
    st.audio(audio_file)
