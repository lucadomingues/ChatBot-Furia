import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração da página
st.set_page_config(page_title="ChatBot Furia", page_icon="Furia_Esports_logo.png")

# Estilizando balões de conversa e a parte de redes sociais
st.markdown("""
    <style>
    [data-testid="stChatMessageContent"] {
        background-color: #f0f2f6;
        padding: 12px 18px;
        border-radius: 15px;
        margin-top: 4px;
        margin-bottom: 10px;
        max-width: 90%;
        display: inline-block;
        font-size: 16px;
    }
    
    #redes_sociais{
        text-align: center;
    }
            
    #linha_redes{
        margin-top: 40px;
        margin-bottom: 10px;
    }
            
    .icones_redes{
        width: 26px;
        margin: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configurações da API
API_KEY = os.getenv("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")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # ou seu domínio real
    "X-Title": "MeuChatBotStreamlit"
}

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": ("Você é um assistente especializado no Clube Esportivo Brasileiro Furia."
                                       "Responda apenas sobre assuntos relacionados ao time de footiball, redram, lol, valorant, r6, sua história, jogadores, títulos, torcida, eventos"
                                       "Se o usuário perguntar qualquer coisa fora desse tema, gentilmente diga que você só pode responder sobre o Clube Esportivo Furia."
                                       "Nunca responda perguntas fora desse assunto.")},
        {"role": "assistant", "content": "Olá! 👋 Sou o assistente virtual da FURIA Esportes. Estou aqui para te ajudar com informações sobre nossos times, produtos, eventos e tudo do mundo FURIA. Bora nessa?"}
    ]

# Exibindo imagem ao lado do titulo usando st.columns
# como a img está salva localmente precisa ser dessa forma
col1, col2 = st.columns([1, 5])
with col1:
    st.image("Furia_Esports_logo.png", width=90)
with col2:
    st.markdown("<h1 style='margin: 0';>Chat da Furia</h1>", unsafe_allow_html=True)


# Entrada do usuário
user_input = st.chat_input("Digite sua mensagem...")


if user_input:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepara e envia para a API
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": st.session_state.messages
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
    else:
        reply = f"❌ Erro {response.status_code}: {response.text}"
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Exibe histórico do chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ícones das Redes Sociais Furia
st.markdown(
    """
    <hr id='linha_redes'>
    <div id='redes_sociais'">
        <a href="https://www.furia.gg/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/841/841364.png" class="icones_redes">
        </a>
        <a href="https://twitter.com/furia" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" class="icones_redes">
        </a>
        <a href="https://www.instagram.com/furiagg" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733558.png" class="icones_redes">
        </a>
        <a href="https://www.youtube.com/@FURIAgg" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" class="icones_redes">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)