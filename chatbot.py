import requests
import streamlit as st

API_KEY = "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"

def enviar_mensagem(mensagem):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost", # Pode deixar http://localhost ou dominio do site
        "X-Title": "ChatBotFuria"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": mensagem}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Verificação: se o código for 200 significa que deu certo e não tem erro
    if response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

historico = [{"role": "system", "content": "Você é um assistente útil e educado."}]

print("=== ChatBot Terminal - Digíte 'SAIR' para encerrar o chat ===")

while True:
    user_input = input("Você: ")
    if user_input.lower() in ["sair", "exit", "quit"]:
        print("Encerrando chat.")
        break

    historico.append({"role": "user", "content": user_input})
    
    try:
        resposta = enviar_mensagem(historico)
        historico.append({"role": "assistant", "content": resposta})
        print(f"Bot: {resposta}\n")
    except Exception as e:
        print(f"Erro: {e}")