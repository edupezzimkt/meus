import ollama

# Função para gerar respostas com o modelo Llama3 mistral-nemo com cache
def gerar_resposta_llama(mensagens, instrucao, model='mistral-nemo', cache={}):
    # Concatena todas as mensagens anteriores para formar a chave do cache
    chave_cache = ' '.join([msg['content'] for msg in mensagens])

    # Verifica se a resposta já está no cache
    if chave_cache in cache:
        return cache[chave_cache]
    
    mensagens_iniciais = [{'role': 'system', 'content': instrucao}]
    mensagens_completa = mensagens_iniciais + mensagens
    stream = ollama.chat(
        model=model,
        messages=mensagens_completa,
        stream=True
    )

    resposta = ''
    for chunk in stream:
        resposta += chunk['message']['content']
    
    # Armazena a resposta no cache
    cache[chave_cache] = resposta
    
    return resposta

if __name__ == '__main__':
    # Defina o prompt inicial
    instrucao = (
        "Você é um assistente divertido e conta piada que vai responder a perguntas gerais."
    )
    
    print('Bem-vindo ao chat! :)')
    
    # Histórico de mensagens
    mensagens = [{'role': 'system', 'content': instrucao}]
    
    # Inicializa o cache
    cache_respostas = {}
    
    while True:
        input_usuario = input('Você: ')
        
        # Verifica se o usuário deseja encerrar a conversa
        if input_usuario.lower() in ['sair', 'encerrar', 'fim', 'obrigado']:
            print('Até já, foi um prazer conversar com você! :)')
            break
        
        # Adiciona a mensagem do usuário ao histórico
        mensagens.append({'role': 'user', 'content': input_usuario})
        
        # Gera a resposta usando o histórico de mensagens e o cache
        resposta = gerar_resposta_llama(mensagens, instrucao, cache=cache_respostas)
        
        # Adiciona a resposta do assistente ao histórico
        mensagens.append({'role': 'assistant', 'content': resposta})
        
        print('Assistente: ', resposta)
