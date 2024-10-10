import streamlit as st
import asyncio
from streamlit_chat import message as msg
import websockets

# Função assíncrona para conectar e enviar mensagens via WebSocket
async def connect_and_chat(user_message):
    uri = "ws://localhost:8000/ws/{user_id}"  # Substituir pelo IP ou URL do servidor WebSocket
    async with websockets.connect(uri) as websocket:
        await websocket.send(user_message)
        response = await websocket.recv()
        return response

# Função para exibir a conversa
def render_chat(hst_conversa):
    for i in range(len(hst_conversa)):
        if i % 2 == 0:
            msg("**PAINe**: " + hst_conversa[i], key=f"bot_msg_{i}")
        else:
            msg("**You**: " + hst_conversa[i], is_user=True, key=f"user_msg_{i}")

# Inicializando o histórico de conversa no session_state
if 'hst_conversa' not in st.session_state:
    st.session_state.hst_conversa = []

# Input do usuário
text_input_center = st.text_input("Digite sua mensagem")

# Botão de enviar
if st.button("Enviar"):
    if text_input_center:
        # Atualiza o histórico local
        st.session_state.hst_conversa.append(f"Você: {text_input_center}")

        # Envia a mensagem via WebSocket e recebe a resposta
        response = asyncio.run(connect_and_chat(text_input_center))
        st.session_state.hst_conversa.append(f"PAINe: {response}")

# Renderiza a conversa no Streamlit
if len(st.session_state.hst_conversa) > 0:
    render_chat(st.session_state.hst_conversa)
