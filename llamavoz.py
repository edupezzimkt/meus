from io import BytesIO
from pathlib import Path

import speech_recognition as sr
from playsound import playsound
import ollama  # Importe a biblioteca para Llama3 local

ARQUIVO_AUDIO = 'fala_assistant.mp3'
recognizer = sr.Recognizer()

def grava_audio():
    with sr.Microphone() as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio(audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'
    transcricao = recognizer.recognize_google(audio, language='pt-BR')
    return transcricao

# Função para gerar respostas com o modelo Llama3
def gerar_resposta_llama(mensagens, instrucao, model='llama3'):
    mensagens_iniciais = [{'role': 'system', 'content': instrucao}]
    mensagens_completa = mensagens_iniciais + mensagens
    stream = ollama.chat(
        model=model,
        messages=mensagens_completa,
        stream=True
    )

    resposta_completa = ""
    for parte in stream:
        # Acessa o 'content' dentro de 'message'
        if 'message' in parte and 'content' in parte['message']:
            resposta_completa += parte['message']['content']
        else:
            print(f"Estrutura inesperada na resposta: {parte}")

    return resposta_completa

def cria_3(texto):
    if Path(ARQUIVO_AUDIO).exists():
        Path(ARQUIVO_AUDIO).unlink()
    resposta = ollama.text_to_speech(texto)  # Supondo que Llama3 suporte TTS localmente
    with open(ARQUIVO_AUDIO, 'wb') as f:
        f.write(resposta)

def roda_audio():
    playsound(ARQUIVO_AUDIO)


if __name__ == '__main__':

    mensagens = []
    instrucao = "Você é um assistente que ajuda a responder perguntas com base em uma conversa de voz."

    while True:
        audio = grava_audio()
        transcricao = transcricao_audio(audio)
        mensagens.append({'role': 'user', 'content': transcricao})
        print(f'User: {mensagens[-1]["content"]}')
        resposta = gerar_resposta_llama(mensagens, instrucao)
        mensagens.append({'role': 'assistant', 'content': resposta})
        print(f'Assistant: {mensagens[-1]["content"]}')
        cria_3(mensagens[-1]["content"])
        roda_audio()
